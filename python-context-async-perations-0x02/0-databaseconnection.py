import sqlite3



class DatabaseConnection:

    def __init__(this, db_name):
        this.db_name = db_name
        this.conn = None

    def __enter__(this):
        """This executes when the with statement starts"""
        this.conn = sqlite3.connect(this.db_name)
        return this.conn


    def __exit__(this, type, value, traceback):
        """This executes when the with statement ends"""
        if type and value and traceback:
            print( "Error occured while connecting to db" )
        if this.conn:
            this.conn.close()
        return True # to avoid carrying over errors
        # Remove for debugging
        
        
with DatabaseConnection( "users.db" ) as conn:
    cursor = conn.cursor()
    cursor.execute( "SELECT * FROM users" )

    result = cursor.fetchall()
    for row in result:
        print(row)
