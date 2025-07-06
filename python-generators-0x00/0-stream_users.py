import mysql.connector

# --- Database Configuration ---
# IMPORTANT: Ensure this matches your MySQL setup and the password you set.
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': input("your mysql password"), # will replace with hidden input
}

DATABASE_NAME = 'ALX_prodev'
TABLE_NAME = 'user_data'


def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL.
    Returns the connection object or None if connection fails.
    """
    try:
        conn = mysql.connector.connect(database=DATABASE_NAME, **DB_CONFIG)
        # print(f"Successfully connected to database '{DATABASE_NAME}'.") # Optional: uncomment for verbose output
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database '{DATABASE_NAME}': {err}")
        print("Ensure the database exists, credentials are correct, and MySQL server is running.")
        return None


def stream_users():
    """
    A generator function that streams rows from the 'user_data' table one by one.
    It connects to the ALX_prodev database, fetches all rows, and yields each row
    as a dictionary. This function uses only one explicit loop for yielding.
    """
    conn = None
    cursor = None
    try:
        # Establish connection to the ALX_prodev database
        conn = connect_to_prodev()
        if not conn:
            # If connection fails, print message and exit the generator
            # The 'return' statement in a generator effectively stops its iteration.
            return

        # Create a cursor to execute SQL queries.
        # dictionary=True makes each fetched row a dictionary, accessible by column name.
        cursor = conn.cursor(dictionary=True)

        # Execute the SELECT query to fetch all data from the user_data table.
        # The cursor itself becomes an iterable that fetches rows as needed.
        select_query = f"SELECT user_id, name, email, age FROM {TABLE_NAME}"
        cursor.execute(select_query)

        # Iterate over the cursor to yield each row.
        # This is the single loop required by the objective.
        print(f"\n--- Streaming data from '{TABLE_NAME}' using generator ---")
        for row in cursor:
            yield row # Yields one row at a time, pausing execution until next() is called.

    except mysql.connector.Error as err:
        print(f"Error during data streaming: {err}")
    finally:
        # Ensure the cursor and connection are closed, regardless of success or failure.
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        # print("Database connection closed.")


if __name__ == "__main__":
    # This block demonstrates how to use the stream_users generator.
    # It will iterate over the yielded rows and print each one.
    for user_data_row in stream_users():
        print(user_data_row)

    print("\nStreaming complete.")
