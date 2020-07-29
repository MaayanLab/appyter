import os
import sys
import json
import click
import asyncio
import socketio
import requests

from appyter.remote.cli import remote
from appyter.util import join_routes, is_remote

def read_chunks(fr, chunk_size=1024*100):
  ''' Read a file in chunks generating the chunks
  '''
  while True:
    data = fr.read(chunk_size)
    if not data:
      break
    yield data

async def get_queue_assert(input_msg_queue, **conditions):
  response = await input_msg_queue.get()
  assert response['type'] not in {'error', 'connection_error', 'disconnect'}, response['data']
  for key, value in conditions.items():
    assert response[key] == value, f"Failure, expected {conditions} got {response}"
  return response

async def do_remote_download(sio, input_msg_queue, output_msg_queue, data):
  ''' Handle submitting a download, and watching it complete on remote.
  '''
  await sio.emit('download_start', data)
  msg = await get_queue_assert(input_msg_queue, type='download_queued')
  await output_msg_queue.put(msg)
  while True:
    msg = await input_msg_queue.get()
    await output_msg_queue.put(msg)
    if msg['type'] == 'download_complete':
      break
    assert msg['type'] == 'download_progress', f"Failure, expected `download_progress` got {msg}"

async def do_remote_upload(sio, input_msg_queue, output_msg_queue, data):
  ''' Handle upload to remote.
  '''
  with open(data['name'], 'rb') as fr:
    # request upload
    await sio.emit('siofu_start', data)
    # wait for server to be ready
    msg = await input_msg_queue.get()
    await output_msg_queue.put(msg)
    assert msg['type'] == 'siofu_ready' and msg['data']['id'] == data['id'], f"Error: received {msg}"
    # read file in chunks
    for chunk in read_chunks(fr):
      await sio.emit('siofu_progress', dict(id=data['id'], content=chunk))
      msg = await input_msg_queue.get()
      await output_msg_queue.put(msg)
      assert msg['type'] == 'siofu_chunk' and msg['data']['id'] == data['id'], f"Error: received {msg}"
  #
  await sio.emit('siofu_done', data)
  msg = await input_msg_queue.get()
  await output_msg_queue.put(msg)
  assert msg['type'] == 'siofu_complete' and msg['data']['id'] == data['id'], f"Error: received {msg}"

async def remote_message_producer(sio, url, input_msg_queue):
  ''' Listen for events and put them on a async queue
  '''
  # Step 1. Capture messages from remote onto a queue for processing
  # socketio
  @sio.on('connect')
  async def _():
    await input_msg_queue.put(dict(type='connect', data=''))
  @sio.on('connect_error')
  async def _(data):
    await input_msg_queue.put(dict(type='connect_error', data=data))
  @sio.on('disconnect')
  async def _():
    await input_msg_queue.put(dict(type='disconnect', data=''))
  # api
  @sio.on('session')
  async def _(data):
    await input_msg_queue.put(dict(type='session', data=data))
  # notebook generation
  @sio.on('status')
  async def _(data):
    await input_msg_queue.put(dict(type='status', data=data))
  @sio.on('progress')
  async def _(data):
    await input_msg_queue.put(dict(type='progress', data=data))
  @sio.on('nb')
  async def _(data):
    await input_msg_queue.put(dict(type='nb', data=data))
  @sio.on('cell')
  async def _(data):
    await input_msg_queue.put(dict(type='cell', data=data))
  @sio.on('error')
  async def _(data):
    await input_msg_queue.put(dict(type='error', data=data))
  # remote download
  @sio.on('download_start')
  async def _(data):
    await input_msg_queue.put(dict(type='download_start', data=data))
  @sio.on('download_queued')
  async def _(data):
    await input_msg_queue.put(dict(type='download_queued', data=data))
  @sio.on('download_complete')
  async def _(data):
    await input_msg_queue.put(dict(type='download_complete', data=data))
  @sio.on('download_error')
  async def _(data):
    await input_msg_queue.put(dict(type='download_error', data=data))
  # remote upload
  @sio.on('siofu_ready')
  async def _(data):
    await input_msg_queue.put(dict(type='siofu_ready', data=data))
  @sio.on('siofu_chunk')
  async def _(data):
    await input_msg_queue.put(dict(type='siofu_chunk', data=data))
  @sio.on('siofu_complete')
  async def _(data):
    await input_msg_queue.put(dict(type='siofu_complete', data=data))
  @sio.on('siofu_error')
  async def _(data):
    await input_msg_queue.put(dict(type='siofu_error', data=data))
  #
  # Step 2. Establish a connection with remote
  await sio.connect(url)
  # wait until disconnect (pushing any received events onto the asyncio queue)
  await sio.wait()

async def evaluate_saga(sio, url, context, params, output, input_msg_queue, output_msg_queue):
  ''' Consume events from remote when necessary
  '''
  try:
    # Ensure we connected properly
    response = await get_queue_assert(input_msg_queue, type='connect')
    # Step 3. Request session on remote
    await sio.emit('session', {})
    response = await get_queue_assert(input_msg_queue, type='session')
    session = response['data']
    # Step 4. Get file(s) onto remote
    for param in params:
      if param['field'] != 'FileField':
        continue
      if param['args']['name'] in context:
        context_value = context[param['args']['name']]
        if is_remote(context_value):
          # have remote download the file
          await do_remote_download(sio, input_msg_queue, output_msg_queue, dict(session, name=param['args']['name'], url=context_value, filename=os.path.basename(context_value)))
        else:
          # upload the file
          await do_remote_upload(sio, input_msg_queue, output_msg_queue, dict(session, id=0, name=context_value))
      else:
        await output_msg_queue.put({ 'type': 'warning', 'data': f"Missing file for `{param['args']['name']}`" })
    # Step 5. Create notebook on remote
    await sio.emit('submit', dict(session, **context))
    # Step 6. Start execution on remote
    await sio.emit('init', session)
    # Process results
    while True:
      response = await get_queue_assert(input_msg_queue)
      await output_msg_queue.put(response)
      if response['type'] == 'status' and response['data'] == 'Success':
        # Step 7. Grab final notebook from remote
        # NOTE: not async but doesn't really matter here..
        response = requests.get(join_routes(url, session['_session'])[1:], headers={'Accept': 'application/json'})
        assert response.status_code <= 299, f"Error ({response.status_code}): {response.text}"
        json.dump(response.json(), output)
        break
  except Exception as e:
    await output_msg_queue.put(dict(type='error', data=str(e)))
  #
  # Step 8. Disconnect from server
  await sio.disconnect()
  await output_msg_queue.put(None)
#
async def output_msg_consumer(output_msg_queue, emit):
  while True:
    msg = await output_msg_queue.get()
    if msg is None:
      break
    print(json.dumps(msg), file=emit)

@remote.command(help='Construct and execute the appyter provided parameters')
@click.option(
  '--context',
  envvar='CONTEXT',
  default='-',
  type=click.Path(readable=True, dir_okay=False, allow_dash=True),
  help='JSON serialized context mapping field names to values (- for stdin)',
)
@click.option(
  '--emit',
  envvar='EMIT',
  default='-',
  type=click.Path(writable=True, dir_okay=False, allow_dash=True),
  help='The output location of the progress stream (- for stderr)',
)
@click.option(
  '--output',
  envvar='OUTPUT',
  default='-',
  type=click.Path(writable=True, dir_okay=False, allow_dash=True),
  help='The output location of the inspection json (- for stdout)',
)
@click.argument('url', envvar='URL')
def nbevaluate(url, context, emit, output):
  context = json.load(sys.stdin if context == '-' else open(context, 'r'))
  emit = sys.stderr if emit == '-' else open(emit, 'w')
  output = sys.stdout if output == '-' else open(output, 'w')
  # Step 1. Inspect remote ensuring it's up and grabbing notebook parameters
  response = requests.get(url, headers={'Accept': 'application/json'})
  assert response.status_code <= 299, f"Error ({response.status_code}): {response.text}"
  params = response.json()
  # Execute async saga for evaluation
  sio = socketio.AsyncClient()
  loop = asyncio.get_event_loop()
  input_msg_queue = asyncio.Queue(loop=loop)
  output_msg_queue = asyncio.Queue(loop=loop)
  loop.run_until_complete(asyncio.gather(
    remote_message_producer(sio, join_routes(url, 'socket.io')[1:], input_msg_queue),
    evaluate_saga(sio, url, context, params, output, input_msg_queue, output_msg_queue),
    output_msg_consumer(output_msg_queue, emit),
  ))
  loop.close()
