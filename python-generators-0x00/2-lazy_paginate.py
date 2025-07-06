import mysql.connector

# --- Database Configuration ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': input("your mysql password"),
}

DATABASE_NAME = 'ALX_prodev'

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

def paginate_users(page_size, offset):
    """
    Fetches a single page of user data from the 'user_data' table.

    Args:
        page_size (int): The maximum number of rows to fetch for this page.
        offset (int): The starting row offset for this page.
    Returns:
        list: A list of dictionaries, where each dictionary represents a user row.
              Returns an empty list if no more records are found.
    """
    if not isinstance(page_size, int) or page_size <= 0:
        raise ValueError("page_size must be a positive integer.")
    if not isinstance(offset, int) or offset < 0:
        raise ValueError("offset must be a non-negative integer.")

    conn = None
    cursor = None
    page_data = []
    try:
        conn = connect_to_prodev()
        if not conn:
            print("Failed to connect to ALX_prodev for pagination.")
            return []

        cursor = conn.cursor(dictionary=True) # Return rows as dictionaries
        # Use LIMIT and OFFSET for pagination
        select_query = "SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s"
        cursor.execute(select_query, (page_size, offset))

        page_data = cursor.fetchall() # Fetch all rows for the current page
        return page_data

    except mysql.connector.Error as err:
        print(f"Error fetching paginated data: {err}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def lazy_paginate(page_size):
    """
    A generator function that lazily loads pages of user data from the 'user_data' table.
    It fetches the next page only when needed, using paginate_users.
    This function uses only one loop.

    Args:
        page_size (int): The number of rows to include in each page.
    Yields:
        list: A list of dictionaries, representing a page of user data.
    """
    if not isinstance(page_size, int) or page_size <= 0:
        raise ValueError("page_size must be a positive integer.")

    offset = 0
    # This is the single loop for the generator
    while True:
        print(f"Fetching page with offset: {offset}")
        page = paginate_users(page_size, offset)

        if not page:
            # If the page is empty, it means there are no more records
            print("No more pages to fetch.")
            break # Exit the loop

        yield page # Yield the current page of data
        offset += page_size # Increment offset for the next page

if __name__ == "__main__":
    # Example usage:
    my_page_size = 2 # Define how many users per page

    print(f"\n--- Lazily loading data in pages of {my_page_size} users ---")

    # Iterate over the pages yielded by the lazy_paginate generator
    page_number = 1
    for page in lazy_paginate(my_page_size):
        print(f"\n--- Displaying Page {page_number} ---")
        if page:
            for user in page:
                print(user)
        else:
            print("Page is empty (this should not happen if the loop breaks correctly).")
        page_number += 1

    print("\nLazy pagination complete.")

