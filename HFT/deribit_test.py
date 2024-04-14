import asyncio
import json
import websockets
import pandas as pd
import pprint

msg = \
{
  "jsonrpc" : "2.0",
  "id" : 7617,
  "method" : "public/get_instruments",
  "params" : {
    "currency" : "BTC",
    "kind" : "option",
    "expired" : False
  }
}

async def call_api(msg):
	async with websockets.connect('wss://test.deribit.com/ws/api/v2') as websocket:
		await websocket.send(msg)
		while websocket.open:
			response = await websocket.recv()
			# do something with the response...
			return json.loads(response)

r = asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg)))
pprint.pprint(r)
