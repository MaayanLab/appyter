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
      'clients': set(),
      'messages': [],
    }
  return rooms[room]

async def remove_client_from_room(room_id, client_id):
  global rooms
  if room_id in rooms:
    rooms[room_id]['clients'].remove(client_id)
    if not rooms[room_id]['clients']:
      # no more clients, close room
      logger.debug(f"closing room {room_id}")
      del rooms[room_id]

async def enter_room(client_id, room_id):
  room = await ensure_room(room_id)
  if client_id not in room['clients']:
    logger.debug(f"client {client_id} joined room {room_id}")
    # add client to room and relay old messages to the client
    room['clients'].add(client_id)
    socketio.enter_room(client_id, room_id)
    for msg in room['messages']:
      await socketio.emit(msg['event'], msg['data'], to=client_id)

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
async def on_join(client_id, room_id):
  await enter_room(client_id, room_id)

@socketio.on('forward')
async def forward(client_id, data):
  global rooms
  if data['to'] in rooms:
    rooms[data['to']]['messages'].append(data)

@socketio.on('disconnect')
async def _(client_id):
  for room in socketio.rooms(client_id):
    await remove_client_from_room(room, client_id)
