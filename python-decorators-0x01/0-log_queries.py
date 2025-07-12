import sqlite3
import functools
from datetime import datetime

#### decorator to lof SQL queries

""" YOUR CODE GOES HERE"""

def log_queries(func):
    """This decorator logs query results."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("-------------------------Logging Starts-------------------------")
        print( datetime.now() )
        result = func(*args, **kwargs)
        for row in result:
            print(row)
        print( datetime.now() )
        print("-------------------------Logging Ends-------------------------")
        return result
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")