import asyncio
import aiosqlite
import time

db = None

async def async_fetch_users():

    """Fetches all the users"""
    start = time.time()
    db.row_factory = aiosqlite.Row
    async with db.execute('SELECT * FROM users') as cursor:
        async for row in cursor:
            print("[ALL USERS]", dict(row))
    end = time.time()
    print( f"Done executing {async_fetch_users.__name__} in {end-start} seconds" )
    return True


async def async_fetch_older_users():

    """Fetches all users with their age above 40"""
    # Seems we have to collect execution time as this executes slower than the other
    start = time.time()
    db.row_factory = aiosqlite.Row
    async with db.execute('SELECT * FROM users WHERE age > 20') as cursor:
        async for row in cursor:
            print("[OLDER USERS]", dict(row))
    end = time.time()
    print( f"Done executing {async_fetch_older_users.__name__} in {end-start} seconds" )
    return True


async def fetch_concurrently():
    """Executes both functions synchronously"""
    global db
    async with aiosqlite.connect("users.db") as database:
        db = database
        await asyncio.gather(
            async_fetch_users(),
            async_fetch_older_users()
        )


if __name__ == "__main__":
    asyncio.run( fetch_concurrently() )
