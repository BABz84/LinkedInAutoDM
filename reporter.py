#!/usr/bin/env python3
"""
reporter.py - Generates a daily summary report of messaging activity.
"""
import db
from datetime import datetime

def generate_report():
    """
    Queries the database and generates a text report for today's activity.
    """
    conn = db.get_db_connection()
    cur = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")
    start_of_day = int(datetime.strptime(today, "%Y-%m-%d").timestamp())

    cur.execute("SELECT * FROM messages WHERE sent_at >= ?", (start_of_day,))
    results = cur.fetchall()
    conn.close()

    report_path = f"results/{today}_report.txt"
    total_sent = 0
    successful_sends = []
    errors = []

    for row in results:
        total_sent += 1
        if row[2] == 'ok':
            successful_sends.append(row[0])
        else:
            errors.append(f"  - Profile {row[0]}: {row[2]}")

    with open(report_path, "w") as f:
        f.write(f"# LinkedIn Auto-Messenger Report for {today}\n\n")
        f.write(f"## Summary\n")
        f.write(f"- Total Messages Processed Today: {total_sent}\n")
        f.write(f"- Successful Messages Sent: {len(successful_sends)}\n")
        f.write(f"- Errors Encountered: {len(errors)}\n\n")

        if successful_sends:
            f.write("## Successful Sends\n")
            for pid in successful_sends:
                f.write(f"  - {pid}\n")
            f.write("\n")

        if errors:
            f.write("## Errors & Issues\n")
            for error in errors:
                f.write(f"{error}\n")
            f.write("\n")

    print(f"Daily report generated at {report_path}")

if __name__ == "__main__":
    generate_report()
