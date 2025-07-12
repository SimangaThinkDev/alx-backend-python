import time
import sqlite3 
import functools

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

""" your code goes here"""
def retry_on_failure(retries=3, delay=1): # setting defaults myself
    def decorator(func):
        functools.wraps(func)
        def wrapper(*args, **kwargs) -> any:
            for attempts in range(retries):
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    pass
            return result
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)