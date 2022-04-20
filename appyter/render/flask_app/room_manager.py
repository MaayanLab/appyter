''' Manage rooms
NOTE: `rooms` state would need to be distributed if the
server was distributed.
'''
import uuid
import contextlib
import logging
logger = logging.getLogger(__name__)

from appyter.render.flask_app.socketio import socketio

rooms = {}

async def ensure_room(room):
  global rooms
  if room not in rooms:
    logger.debug(f"creating room {room}")
    rooms[room] = {
      'users': {},
      'clients': set(),
      'messages': [],
    }
  return rooms[room]

async def remove_client_from_room(room_id, client_sid):
  global rooms
  if room_id in rooms:
    rooms[room_id]['clients'].remove(client_sid)
    if not rooms[room_id]['clients']:
      # no more clients, close room
      logger.debug(f"closing room {room_id}")
      del rooms[room_id]

async def enter_room(client_sid, room_id):
  room = await ensure_room(room_id)
  if client_sid not in room['clients']:
    logger.debug(f"client {client_sid} joined room {room_id}")
    # add client to room and relay old messages to the client
    room['clients'].add(client_sid)
    socketio.enter_room(client_sid, room_id)
    async with socketio.session(client_sid) as client_sess:
      client_uid = client_sess['uid']
    for msg in room['messages'][room['users'].get(client_uid, 0):]:
      await socketio.emit(msg['event'], msg['data'], to=client_sid)
    room['users'][client_uid] = len(room['messages'])

async def ensure_joined(client_sid):
  async with socketio.session(client_sid) as client_sess:
    client_uid = client_sess['uid']
  #
  for room_id in rooms:
    if client_uid in rooms[room_id]['users']:
      await enter_room(client_sid, room_id)

async def find_room(room_id):
  global rooms
  return room_id in rooms

@contextlib.asynccontextmanager
async def room_lock(room_id):
  lock_id = str(uuid.uuid4())
  room = await ensure_room(room_id)
  room['clients'].add(lock_id)
  try:
    yield
  finally:
    await remove_client_from_room(room_id, lock_id)


@socketio.on('join')
async def on_join(client_sid, room_data):
  if type(room_data) == str: room_data = {'_id': room_data}
  await enter_room(client_sid, room_data['_id'])

@socketio.on('forward')
async def forward(client_sid, data):
  global rooms
  if data['to'] in rooms:
    rooms[data['to']]['messages'].append(data)

@socketio.on('disconnect')
async def _(client_sid):
  for room in socketio.rooms(client_sid):
    await remove_client_from_room(room, client_sid)
