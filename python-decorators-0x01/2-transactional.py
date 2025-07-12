import sqlite3 
import functools


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

def transactional(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not args:
            raise ValueError("Transactional expects a [conn] args to be passed through it")
        conn = args[0]
        try:
            # Explicitly begin a transaction (only if isolation_level=None)
            print(f"[{func.__name__}] Transaction started.")
            result = func(*args, **kwargs) # Call the actual function
            # If no error, commit the transaction
            conn.commit()
            print(f"[{func.__name__}] Transaction committed.")
            return result
        except Exception as e:
            if conn:
                conn.rollback()
                print(f"[{func.__name__}] Transaction rolled back due to error: {e}")
    return wrapper


@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
    #### Update user's email with automatic transaction handling 


update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')