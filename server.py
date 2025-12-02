import asyncio #coroutines and event loops
import websockets #building servers and clients
#import django #handles multiple channels

clients = set() #stores active connections
#userGroup = 0; #default group


async def handle(ws): #registers client and listens for messages
    clients.add(ws)
    try:
        async for msg in ws:
            await asyncio.gather(*[ #broadcasts message to other clients
                c.send(msg) for c in clients if c != ws])
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        clients.remove(ws) #disconnects client

#async def groupchat(msg):
#    print(msg, "45")

async def main():
    async with websockets.serve(handle, "localhost", 11037): #starts server
        print("Server running at ws://localhost:11037")
        await asyncio.Future()   #run forever

if __name__ == "__main__": #runs asynchronous coroutine
    asyncio.run(main())
