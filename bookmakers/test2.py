import asyncio
from bookmakers.Sbobet import Sbobet
import time



async def getpage(loop):
    print("start to create object")
    fut = loop.run_in_executor(None, Sbobet)
    resp = await fut
    print("sbobet object was created. Starting to getting page")
    loop.stop()


loop = asyncio.get_event_loop()

loop.run_until_complete(getpage(loop))

loop.close()