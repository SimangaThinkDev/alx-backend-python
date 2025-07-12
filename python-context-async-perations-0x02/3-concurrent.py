import asyncio, aiosqlite, time

print(aiosqlite.__version__)

"""
async with aiosqlite.connect(...) as db:
    db.row_factory = aiosqlite.Row
    async with db.execute('SELECT * FROM some_table') as cursor:
        async for row in cursor:
            value = row['column']

    await db.execute('INSERT INTO foo some_table')
    assert db.total_changes > 0
"""

async def async_fetch_users(db):
    """Fetches all the users"""
    start = time.time()
    db.row_factory = aiosqlite.Row
    async with db.execute('SELECT * FROM users') as cursor:
        async for row in cursor:
            print("[ALL USERS]", dict(row))
    end = time.time()
    print( f"Done executing {async_fetch_users.__name__} in {end-start} seconds" )
    return True


async def async_fetch_older_users(db):
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
    async with aiosqlite.connect("users.db") as db:
        await asyncio.gather(
            async_fetch_users(db),
            async_fetch_older_users(db)
        )


if __name__ == "__main__":
    asyncio.run( fetch_concurrently() )
