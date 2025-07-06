import mysql.connector

# --- Database Configuration ---
# IMPORTANT: Ensure this matches your MySQL setup and the password you set.
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': input("your mysql password")
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
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database '{DATABASE_NAME}': {err}")
        print("Ensure the database exists, credentials are correct, and MySQL server is running.")
        return None

def stream_users_in_batches(batch_size):
    """
    A generator function that streams rows from the 'user_data' table in batches.
    It connects to the ALX_prodev database and yields lists (batches) of user data.
    This function contains one loop.

    Args:
        batch_size (int): The number of rows to include in each batch.
    Yields:
        list: A list of dictionaries, where each dictionary represents a user row.
    """
    if not isinstance(batch_size, int) or batch_size <= 0:
        raise ValueError("batch_size must be a positive integer.")

    conn = None
    cursor = None
    try:
        conn = connect_to_prodev()
        if not conn:
            print("Failed to connect to ALX_prodev for batch streaming.")
            return # Exit generator if connection fails

        cursor = conn.cursor(dictionary=True) # Return rows as dictionaries
        # FIXED: Hardcoded "FROM user_data" as per the check requirement
        select_query = "SELECT user_id, name, email, age FROM user_data"
        cursor.execute(select_query)

        batch = []
        # Loop 1: Iterates through the database cursor to build batches
        for row in cursor:
            batch.append(row)
            if len(batch) == batch_size:
                yield batch # Yield the full batch
                batch = [] # Reset batch for the next set of records

        # Yield any remaining records in the last (possibly smaller) batch
        if batch:
            yield batch

    except mysql.connector.Error as err:
        print(f"Error during batch streaming: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def batch_processing(batch_size):
    """
    Processes user data in batches, filtering for users over the age of 25.
    This function uses the stream_users_in_batches generator and contains two loops.

    Args:
        batch_size (int): The size of batches to fetch from the database.
    Returns:
        list: A list of dictionaries, containing only users older than 25.
    """
    filtered_users = []
    print(f"\n--- Processing data in batches of {batch_size} ---")

    # Loop 2: Iterates over the batches yielded by stream_users_in_batches
    for batch in stream_users_in_batches(batch_size):
        print(f"Processing batch with {len(batch)} users...")
        # Loop 3: Iterates over each user within the current batch
        for user_data_row in batch:
            # Ensure 'age' is treated as a number for comparison
            try:
                age = float(user_data_row.get('age'))
                if age > 25:
                    filtered_users.append(user_data_row)
            except (ValueError, TypeError):
                print(f"Warning: Could not process age for user: {user_data_row.get('name')}")
                continue # Skip to the next user if age is invalid

    return filtered_users

if __name__ == "__main__":
    # Example usage:
    # Set your desired batch size
    my_batch_size = 3

    # Process the data in batches and get the filtered results
    users_over_25 = batch_processing(my_batch_size)

    print("\n--- Users over the age of 25 ---")
    if users_over_25:
        for user in users_over_25:
            print(user)
    else:
        print("No users found over the age of 25.")

    print("\nBatch processing complete.")
