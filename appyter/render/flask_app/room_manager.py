''' Manage rooms
NOTE: `rooms` state would need to be distributed if the
server was distributed.
'''
from appyter.render.flask_app.socketio import socketio

rooms = {}

async def enter_room(sid, room):
  global rooms
  if room not in rooms:
    rooms[room] = {
      'clients': set(),
      'messages': [],
    }
  if sid not in rooms[room]['clients']:
    # add client to room and relay old messages to the client
    rooms[room]['clients'].add(sid)
    socketio.enter_room(sid, room)
    for msg in rooms[room]['messages']:
      await socketio.emit(*msg, to=sid)

@socketio.on('join')
async def on_join(sid, room):
  await enter_room(sid, room)

@socketio.on('forward')
async def forward(sid, data):
  global rooms
  if data['to'] in rooms:
    rooms[data['to']]['messages'].append((type, data))

@socketio.on('disconnect')
async def _(sid):
  global rooms
  for room in socketio.rooms(sid):
    if room in rooms:
      if sid in rooms[room]['clients']:
        rooms[room]['clients'].remove(sid)
      if not rooms[room]['clients']:
        # no more clients, close room
        del rooms[room]
