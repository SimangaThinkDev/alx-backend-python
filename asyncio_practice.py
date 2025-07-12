import asyncio, time

async def say_hello(name, delay):

    time_result  = None
    start = time.time()

    print( rf"Hello, {name}\nAsyncio running, waiting on delay time to finish execution\n\
          {asyncio.get_running_loop().time():.2f}s" )
    await asyncio.sleep( delay )
    print( rf"Hello, {name}\nAsyncio done executing\n\
          {asyncio.get_running_loop().time():.2f}s" )
    
    end = time.time()

    return end - start # time elapsed
    

async def one_after_another():
    """Task"""
    print( "program started" )

    await say_hello( "Smanga", 2 )
    await say_hello( "Tom", 3 )

    print("Program finished")

async def sync_gather():
    """Task"""
    time_result: float = None
    start = time.time()

    print("Program started")
    results = await asyncio.gather(
        say_hello( "Smanga", 22 ),
        say_hello( "Bob", 19 )
    )

    end = time.time()
    time_result = end - start
    print( f"Programs finished running in {time_result}" )
    
async def make_tasks():
    """Task manager"""

    task1 = asyncio.create_task( say_hello("Simangaliso", 2) )
    task2 = asyncio.create_task( say_hello("Bob", 7) )

    print( "Tasks have been scheduled, now waiting for other tasks" )
    await asyncio.sleep(1)
    print( "Done executing other tasks, now executing scheduled tasks" )

    result1 = await task1
    result2 = await task2

    print( f"Main program finished\nTime elapsed:\n    task1 > {result1}\ntask2 > {result2}" )


if __name__ == "__main__":
    asyncio.run(make_tasks())
