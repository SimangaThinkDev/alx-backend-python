import asyncio

async def say_hello(name, delay):

    print( rf"Hello, {name}\nAsyncio running, waiting on delay time to finish execution\n\
          {asyncio.get_running_loop().time():.2f}s" )
    await asyncio.sleep( delay )
    print( rf"Hello, {name}\nAsyncio done executing\n\
          {asyncio.get_running_loop().time():.2f}s" )
    
async def main():
    """Task"""
    print( "program started" )

    await say_hello( "Smanga" )
    await say_hello( "Smanga" )

    print("Program finished")

if __name__ == "__main__":
    asyncio.run( main() )