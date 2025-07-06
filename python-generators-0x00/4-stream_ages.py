import mysql.connector

# --- Database Configuration ---
# IMPORTANT: Ensure this matches your MySQL setup and the password you set.
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': input("your mysql password"),
}

DATABASE_NAME = 'ALX_prodev'
TABLE_NAME = 'user_data' # Explicitly define table name for clarity

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

def stream_user_ages():
    """
    A generator function that streams user ages one by one from the 'user_data' table.
    It connects to the ALX_prodev database and yields each user's age.
    This function contains one loop.

    Yields:
        float: The age of a user.
    """
    conn = None
    cursor = None
    try:
        conn = connect_to_prodev()
        if not conn:
            print("Failed to connect to ALX_prodev for streaming ages.")
            return # Exit generator if connection fails

        cursor = conn.cursor(dictionary=True) # Return rows as dictionaries
        # Fetch only the age column to minimize data transfer
        select_query = f"SELECT age FROM {TABLE_NAME}"
        cursor.execute(select_query)

        # Loop 1: Iterates through the database cursor to yield ages
        for row in cursor:
            try:
                # Ensure age is converted to a float/decimal type before yielding
                age = float(row.get('age'))
                yield age
            except (ValueError, TypeError):
                print(f"Warning: Skipping invalid age value: {row.get('age')}")
                continue # Skip to the next row if age is invalid

    except mysql.connector.Error as err:
        print(f"Error during age streaming: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def calculate_average_age():
    """
    Calculates the average age of users by streaming ages from the database
    without loading the entire dataset into memory.
    This function uses one loop to iterate over the generator.

    Returns:
        float: The calculated average age, or 0.0 if no ages are found.
    """
    total_age = 0.0
    user_count = 0

    # Loop 2: Iterates over the ages yielded by the stream_user_ages generator
    for age in stream_user_ages():
        total_age += age
        user_count += 1

    if user_count > 0:
        average_age = total_age / user_count
        return average_age
    else:
        return 0.0 # Return 0 if no users or ages were found

if __name__ == "__main__":
    print("\n--- Calculating average age using memory-efficient generators ---")

    average_age = calculate_average_age()

    print(f"Average age of users: {average_age:.2f}") # Format to 2 decimal places

    print("\nAverage age calculation complete.")
