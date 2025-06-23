import sqlite3
import time
import pytest
from queue_builder import build_queue

@pytest.fixture
def db_connection():
    """
    Creates a temporary, in-memory database for testing.
    """
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    # Create the necessary tables
    cursor.execute('''
        CREATE TABLE fs_connections (
            profile_id TEXT PRIMARY KEY,
            first_name TEXT,
            accepted_at TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE messages (
            profile_id TEXT PRIMARY KEY,
            sent_at TIMESTAMP,
            status TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE queue (
            profile_id TEXT PRIMARY KEY,
            first_name TEXT,
            accepted_at TIMESTAMP
        )
    ''')
    yield conn
    conn.close()

def test_delay_filter(db_connection):
    """
    Tests that the queue builder correctly filters out connections that were
    accepted less than 48 hours ago.
    """
    cursor = db_connection.cursor()

    # Add a dummy connection that was accepted 24 hours ago
    twenty_four_hours_ago = time.time() - (24 * 60 * 60)
    cursor.execute('''
        INSERT INTO fs_connections (profile_id, first_name, accepted_at)
        VALUES (?, ?, ?)
    ''', ('12345', 'Test', twenty_four_hours_ago))
    db_connection.commit()

    # Run the queue builder
    build_queue()

    # Check that the queue is empty
    cursor.execute("SELECT * FROM queue")
    assert len(cursor.fetchall()) == 0
