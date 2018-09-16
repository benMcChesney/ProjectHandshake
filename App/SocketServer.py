#!/usr/bin/env python
# WS server example for old Python versions
# example from: https://websockets.readthedocs.io/en/stable/intro.html

import asyncio
import websockets

@asyncio.coroutine
def receive_face(websocket, path):

    name = yield from websocket.recv()
    print("< Face recieved with ID of {}!".format(name))

    # return status
    recieved_message = "face success! ID of {}".format(name)
    yield from websocket.send(recieved_message)

print('Handshake Socket Server starting up....')
print('on localhost:8765')
start_server = websockets.serve(receive_face, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()