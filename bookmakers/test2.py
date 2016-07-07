import asyncio
from bookmakers.sbobet import Sbobet
import time

async def getpage(loop):
    print("start to create object")
    sb = await Sbobet()
    print("sbobet object was created. Starting to getting page")
    result = await sb._get_page("https://www.sbobet.com/euro/football")
    print(result)
    loop.stop()


async def eachsec():
    print("I print info each second!")
    await time.sleep(1)

loop = asyncio.get_event_loop()
coro = getpage(loop)
coro2 = eachsec()
loop.call_soon(coro)
loop.call_soon(eachsec)
loop.run_forever()
loop.close()