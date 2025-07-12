import requests, time, aiohttp, asyncio

def process_request(request: str):
    start = time.time()
    print("Starting to process requests")
    result = requests.get( request )
    end = time.time()
    print(f"Done processing request, elapsed: {end - start}")
    return result


async def fetch_page_async(session, url):
    start = time.time()
    print( f"--------Fetching {url} at {start}----------" )
    async with session.get(url) as response:
        end = time.time()
        text = await response.text()
        return text
    
async def main_async_io():

    async with aiohttp.ClientSession() as session:
        await asyncio.gather(
            fetch_page_async(session, "https://savanna.alxafrica.com/projects/101621"),
            fetch_page_async(session, "https://github.com/SimangaThinkDev/csv_database_alx"),
            fetch_page_async(session, "https://www.python.org/docs")
            )
    print( "All pages fetched asynchronously" )

# But theres a loss of result
# We cannot print out what we are receiving from these pages...

if __name__ == "__main__":
    
    # result = process_request("https://savanna.alxafrica.com/projects/101621")
    # print( result )

    asyncio.run( main_async_io() )