import asyncio

async def func2():
    print("func2 started")
    await asyncio.sleep(15)
    print("func2 ended")
    return  "hai 2"

async def func4():
    print("func4 started")
    await asyncio.sleep(15)
    print("func4 ended")
    return  "hai 4" 

async def func3():
    print("func3 started")
    await asyncio.sleep(30)
    await func4()
    print("func3 ended")
    return  "hai 3 "


async def func1():
    task = asyncio.create_task(func2())
    print("func1 started)")
    asyncio.sleep(10)
    print("hai")
    await func3()
    print("func1 ended")
    task_result = await task
    print("func2 task result:", task_result)
    print("hai")



if __name__ == "__main__":
    asyncio.run(func1())