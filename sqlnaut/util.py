import sqlite3
import csv
import sys

def list_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [row[0] for row in cursor.fetchall()]

def view_table_as_csv(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    if rows:
        csv_writer = csv.writer(sys.stdout)
        csv_writer.writerow([i[0] for i in cursor.description])  # column headers
        csv_writer.writerows(rows)
    else:
        print(f"No data in {table_name}")

def main(db_path):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        tables = list_tables(cursor)
        print("Enter 'ls' to list all tables, a table name to view it as CSV, or 'exit' to quit.")

        while True:
            command = input("Command: ").strip().lower()
            if command == 'exit':
                break
            elif command == 'ls':
                print("\nTables in the database:")
                for table in tables:
                    print(table)
                print()
            elif command in tables:
                view_table_as_csv(cursor, command)
            else:
                print("Unknown command or table not found. Please try again.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python view_sqlite.py <path_to_database>")
    else:
        main(sys.argv[1])

