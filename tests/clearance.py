import asyncio
async def func2():
    print("func2 started")
    asyncio.sleep(15)
    print("func2 ended")
    return  "hai 2"

async def func1():
    print("started ")
    asyncio.run(func2())
    asyncio.sleep(10)
    print("hai")
    await func2()
    print("ended")

asyncio.run(func1())