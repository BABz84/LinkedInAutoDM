import sqlite3
import time

def build_queue():
    """
    Builds a queue of LinkedIn connections to message.

    This function connects to the local SQLite database and retrieves a list of
    connections that were accepted at least 48 hours ago and have not yet been
    messaged. The results are then inserted into the 'queue' table.
    """
    conn = sqlite3.connect('linkedin.db')
    cursor = conn.cursor()

    # Create the queue table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS queue (
            profile_id TEXT PRIMARY KEY,
            first_name TEXT,
            accepted_at TIMESTAMP
        )
    ''')

    # Get connections that were accepted at least 48 hours ago and have not been messaged
    forty_eight_hours_ago = time.time() - (48 * 60 * 60)
    cursor.execute('''
        SELECT c.profile_id, c.first_name, c.accepted_at
        FROM fs_connections c
        LEFT JOIN messages m ON c.profile_id = m.profile_id
        WHERE m.profile_id IS NULL AND c.accepted_at <= ?
    ''', (forty_eight_hours_ago,))
    connections = cursor.fetchall()

    # Add new connections to the queue
    for conn_row in connections:
        cursor.execute('''
            INSERT OR IGNORE INTO queue (profile_id, first_name, accepted_at)
            VALUES (?, ?, ?)
        ''', (conn_row[0], conn_row[1], conn_row[2]))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    build_queue()
