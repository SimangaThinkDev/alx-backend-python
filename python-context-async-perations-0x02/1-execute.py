import sqlite3

class ExecuteQuery:

    def __init__(this, db_name, query):
        this.db_name = db_name
        this.query = query
        this.db, this.cursor = None, None

    def __enter__(this):
        """This executes when the with statement starts"""
        this.conn = sqlite3.connect(this.db_name)
        this.cursor = this.conn.cursor()
        this.cursor.execute(this.query)
        return this.cursor.fetchall()
    
    def __exit__(this, type, value, traceback):
        """This executes when the with statement ends"""
        if type and value and traceback:
            print( "Error occured while connecting to db" )
        if this.conn:
            this.conn.close()
        return True # to avoid carrying over errors
        # Remove for debugging

database = "users.db"
query = "SELECT * FROM users WHERE age > ?"

with ExecuteQuery( "users.db", "SELECT * FROM users WHERE age > ?" ) as result:
    for row in result:
        print( row )


