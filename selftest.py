#!/usr/bin/env python3
"""
selftest.py - A health check script to verify the application's configuration.
"""
import os
import pathlib
import sqlite3
from dotenv import load_dotenv

def run_health_check():
    """
    Performs a series of checks to ensure the application is configured correctly.
    """
    print("Running LinkedIn Auto-Messenger Health Check...")
    checks_passed = True

    # 1. Check for config.py
    print("\n[1/4] Checking for config.py...")
    if pathlib.Path("config.py").exists():
        print("  [+] OK: config.py found.")
    else:
        print("  [-] FAIL: config.py not found. Please ensure the file exists.")
        checks_passed = False

    # 2. Check for .env file and required variables
    print("\n[2/4] Checking for .env file and credentials...")
    if pathlib.Path(".env").exists():
        print("  [+] OK: .env file found.")
        load_dotenv()
        username = os.getenv("LI_USERNAME")
        password = os.getenv("LI_PASSWORD")
        if username and password:
            print("  [+] OK: LI_USERNAME and LI_PASSWORD are set.")
        else:
            print("  [-] FAIL: LI_USERNAME and/or LI_PASSWORD not set in .env file.")
            checks_passed = False
    else:
        print("  [-] FAIL: .env file not found. Please copy .env.example to .env and fill it out.")
        checks_passed = False

    # 3. Check for session.cookie
    print("\n[3/4] Checking for session cookie...")
    if pathlib.Path("session.cookie").exists():
        print("  [+] OK: session.cookie found. You have an active session.")
    else:
        print("  [-] FAIL: session.cookie not found. Please run 'python auth.py' to log in.")
        checks_passed = False

    # 4. Check for database and schema
    print("\n[4/4] Checking database integrity...")
    db_path = pathlib.Path("data.sqlite3")
    if db_path.exists():
        print("  [+] OK: Database file (data.sqlite3) found.")
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = {row[0] for row in cur.fetchall()}
            required_tables = {"connections", "messages"}
            if required_tables.issubset(tables):
                print("  [+] OK: Required tables ('connections', 'messages') exist.")
            else:
                print(f"  [-] FAIL: Database is missing required tables. Found: {tables}")
                checks_passed = False
            conn.close()
        except Exception as e:
            print(f"  [-] FAIL: An error occurred while checking the database: {e}")
            checks_passed = False
    else:
        print("  [-] FAIL: Database file (data.sqlite3) not found. Run db.py to create it.")
        checks_passed = False

    # --- Final Summary ---
    print("\n-----------------------------------------")
    if checks_passed:
        print("✅ Health check passed. Configuration looks good!")
    else:
        print("❌ Health check failed. Please address the issues listed above.")
    print("-----------------------------------------")

if __name__ == "__main__":
    run_health_check()
