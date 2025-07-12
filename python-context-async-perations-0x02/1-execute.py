import sqlite3

class ExecuteQuery:

    def __init__(self, db_name, query):
        self.db_name = db_name
        self.query = query
        self.db, self.cursor = None, None

    def __enter__(self):
        """self executes when the with statement starts"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query)
        return self.cursor.fetchall()
    
    def __exit__(self, type, value, traceback):
        """self executes when the with statement ends"""
        if type and value and traceback:
            print( "Error occured while connecting to db" )
        if self.conn:
            self.conn.close()
        return True # to avoid carrying over errors
        # Remove for debugging

database = "users.db"
query = "SELECT * FROM users WHERE age > ?"

with ExecuteQuery( "users.db", "SELECT * FROM users WHERE age > ?" ) as result:
    for row in result:
        print( row )


