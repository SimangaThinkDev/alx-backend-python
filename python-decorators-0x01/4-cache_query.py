import time
import sqlite3 
import functools


query_cache:dict = {}
previous_query:str = None

#### paste your with_db_decorator here
def with_db_connection(func):
    """ your code goes here"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        result = func( conn, **kwargs )
        conn.close()
        return result
    return wrapper

"""your code goes here"""
def cache_query(func):
    def wrapper(*args, **kwargs):
        global query_cache, previous_query
        """Do something"""
        new_query:str = kwargs['query']
        if previous_query and new_query and new_query.lower() == previous_query.lower():
            print( "\n---------------------------Cache hit.-------------------------\n" )
            return query_cache
        print( "\n-----------------Cache miss -- executing query----------------\n" )
        result = func( *args, **kwargs )
        query_cache = result
        previous_query = new_query
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
for user in users:
    print(user)

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
for user in users_again:
    print(user)