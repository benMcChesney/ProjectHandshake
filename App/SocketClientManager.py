#!/usr/bin/env python

# WS client example for old Python versions

import asyncio
import websockets

@asyncio.coroutine
def send_face( message ):
    websocket = yield from websockets.connect(
        'ws://localhost:8765/')

    try:
        # name = input("What's your name? ")

        yield from websocket.send(message)
        print("> {}".format(message))

        greeting = yield from websocket.recv()
        print("< {}".format(greeting))

    finally:
        yield from websocket.close()