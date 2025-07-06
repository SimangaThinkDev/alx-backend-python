import mysql.connector
import csv
import uuid # For UUID type understanding, though CSV provides them

# --- Database Configuration ---
# IMPORTANT: Replace with your MySQL credentials
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': input("Your MySQL shell password\n>>"), # will replace this with hidden input
}

DATABASE_NAME = 'ALX_prodev'
TABLE_NAME = 'user_data'
CSV_FILE_PATH = 'user_data.csv'


def connect_db():
    """
    Connects to the MySQL database server (without specifying a database initially).
    Returns the connection object or None if connection fails.
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("Successfully connected to MySQL server.")
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL server: {err}")
        print("Please ensure MySQL server is running and credentials are correct.")
        return None


def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist.
    Requires a connection to the MySQL server (not a specific database).
    """
    if not connection:
        print("No database connection provided to create database.")
        return False
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
        print(f"Database '{DATABASE_NAME}' ensured to exist.")
        return True
    except mysql.connector.Error as err:
        print(f"Error creating database '{DATABASE_NAME}': {err}")
        return False
    finally:
        if cursor:
            cursor.close()


def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL.
    Returns the connection object or None if connection fails.
    """
    try:
        conn = mysql.connector.connect(database=DATABASE_NAME, **DB_CONFIG)
        print(f"Successfully connected to database '{DATABASE_NAME}'.")
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database '{DATABASE_NAME}': {err}")
        print("Ensure the database exists and credentials are correct.")
        return None


def create_table(connection):
    """
    Creates a table user_data if it does not exist with the required fields.
    Requires a connection to the ALX_prodev database.
    """
    if not connection:
        print("No database connection provided to create table.")
        return False
    cursor = None
    try:
        cursor = connection.cursor()
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5, 2) NOT NULL,
            INDEX (user_id)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print(f"Table '{TABLE_NAME}' ensured to exist.")
        return True
    except mysql.connector.Error as err:
        print(f"Error creating table '{TABLE_NAME}': {err}")
        return False
    finally:
        if cursor:
            cursor.close()


def insert_data(connection, data):
    """
    Inserts data into the user_data table if it does not exist.
    Requires a connection to the ALX_prodev database and a list of data rows.
    """
    if not connection:
        print("No database connection provided to insert data.")
        return False
    cursor = None
    try:
        cursor = connection.cursor()

        # Check if table is empty before populating to avoid duplicates on re-run
        cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
        if cursor.fetchone()[0] > 0:
            print(f"Table '{TABLE_NAME}' already contains data. Skipping population.")
            return True # Data already exists, so consider it successful

        insert_query = f"""
        INSERT INTO {TABLE_NAME} (user_id, name, email, age)
        VALUES (%s, %s, %s, %s)
        """
        for row in data:
            try:
                # Ensure age is converted to a float/decimal type
                age = float(row['age'])
                values = (
                    row['user_id'],
                    row['name'],
                    row['email'],
                    age
                )
                cursor.execute(insert_query, values)
            except ValueError as ve:
                print(f"Skipping row due to data conversion error: {row} - {ve}")
            except mysql.connector.Error as insert_err:
                print(f"Error inserting row {row}: {insert_err}")
        connection.commit()
        print(f"Data successfully populated into '{TABLE_NAME}'.")
        return True
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
        return False
    finally:
        if cursor:
            cursor.close()


def stream_user_data():
    """
    A generator function that streams rows from the 'user_data' table one by one.
    Yields each row as a dictionary.
    """
    conn = None
    cursor = None
    try:
        conn = connect_to_prodev()
        if not conn:
            print("Failed to connect to ALX_prodev for streaming.")
            return # Exit generator if connection fails

        cursor = conn.cursor(dictionary=True) # Return rows as dictionaries
        cursor.execute(f"SELECT user_id, name, email, age FROM {TABLE_NAME}")

        print("\n--- Streaming data from database using generator ---")
        for row in cursor:
            yield row
    except mysql.connector.Error as err:
        print(f"Error streaming data: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    # Step 1: Connect to the MySQL server
    server_conn = connect_db()
    if not server_conn:
        exit(1)

    # Step 2: Create the database
    if not create_database(server_conn):
        server_conn.close()
        exit(1)
    server_conn.close() # Close the server connection after database creation

    # Step 3: Connect to the ALX_prodev database
    prodev_conn = connect_to_prodev()
    if not prodev_conn:
        exit(1)

    # Step 4: Create the table
    if not create_table(prodev_conn):
        prodev_conn.close()
        exit(1)

    # Step 5: Read data from CSV
    csv_data = []
    try:
        with open(CSV_FILE_PATH, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                csv_data.append(row)
    except FileNotFoundError:
        print(f"Error: CSV file '{CSV_FILE_PATH}' not found.")
        prodev_conn.close()
        exit(1)

    # Step 6: Insert data into the table
    if not insert_data(prodev_conn, csv_data):
        prodev_conn.close()
        exit(1)

    prodev_conn.close() # Close the connection after all setup/insertion

    # Step 7: Demonstrate the generator (will establish its own connection)
    for user_row in stream_user_data():
        print(user_row)

    print("\nGenerator demonstration complete.")
