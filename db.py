import sqlite3
import pathlib

DB_PATH = pathlib.Path(__file__).parent / "data.sqlite3"

def get_db_connection():
    """Establishes and returns a database connection."""
    return sqlite3.connect(DB_PATH)

def setup_database():
    """
    Creates the necessary database tables if they do not already exist.
    This function should be called once during the initial setup.
    """
    print("Setting up database...")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS connections(
          profile_id TEXT PRIMARY KEY,
          first_name TEXT,
          accepted_at INTEGER
        );
        CREATE TABLE IF NOT EXISTS messages(
          profile_id TEXT PRIMARY KEY,
          sent_at    INTEGER,
          status     TEXT
        );
    """)
    conn.commit()
    conn.close()
    print("Database setup complete.")

# For scripts that need to perform database operations,
# they can now do the following:
#
# import db
# conn = db.get_db_connection()
# cur = conn.cursor()
# ... perform operations ...
# conn.commit()
# conn.close()

if __name__ == '__main__':
    setup_database()
