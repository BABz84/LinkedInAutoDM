import sqlite3

def initialize_database():
    """
    Initializes the SQLite database and creates the necessary tables.

    This function creates the 'messages', 'queue', and 'fs_connections' tables
    if they don't already exist.
    """
    conn = sqlite3.connect('linkedin.db')
    cursor = conn.cursor()

    # Create the messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            profile_id TEXT PRIMARY KEY,
            sent_at TIMESTAMP
        )
    ''')

    # Create the queue table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS queue (
            profile_id TEXT PRIMARY KEY,
            first_name TEXT,
            accepted_at TIMESTAMP
        )
    ''')

    # Create the fs_connections table (for demonstration purposes)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fs_connections (
            profile_id TEXT PRIMARY KEY,
            first_name TEXT,
            accepted_at TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    initialize_database()
