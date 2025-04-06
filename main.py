import sqlite3
from database import connect_db, get_tables, execute_query
from csv_loader import create_table_from_csv
from crud import create_record, read_records, update_record, delete_record
from ai_assistant import generate_sql_from_nl
from utils import log_error

def display_records(records):
    """Display records in a simple row-by-row format."""
    if records:
        for row in records:
            print(row)
    else:
        print("No records found.")

def main():
    conn = connect_db()
    print("Welcome to the Chat SQL Application!")
    
    while True:
        print("\nCommands: load, query, list, create, read, update, delete, exit")
        command = input("Enter command: ").strip().lower()
        
        if command == "load":
            csv_path = input("Enter CSV file path: ").strip()
            try:
                create_table_from_csv(csv_path, conn)
            except Exception as e:
                print(f"Failed to load CSV: {e}")
                
        elif command == "query":
            nl_query = input("Enter your natural language query: ").strip()
            try:
                sql_query, explanation = generate_sql_from_nl(nl_query, conn)
                print("\nGenerated SQL Query:")
                print(sql_query)
                print("\nExplanation:")
                print(explanation)
                cursor = execute_query(conn, sql_query)
                rows = cursor.fetchall()
                print("\nQuery Results:")
                display_records(rows)
            except Exception as e:
                print(f"Error processing query: {e}")
                
        elif command == "list":
            tables = get_tables(conn)
            print("Tables in the database:")
            for table in tables:
                print(table)
                
        elif command == "create":
            table = input("Enter table name to insert record: ").strip()
            # Fetch column info to guide user input
            cursor = execute_query(conn, f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            if not columns:
                print(f"Table '{table}' does not exist.")
                continue
            data = {}
            for col in columns:
                col_name = col[1]
                value = input(f"Enter value for '{col_name}': ")
                data[col_name] = value
            create_record(conn, table, data)
            
        elif command == "read":
            table = input("Enter table name to read records: ").strip()
            condition = input("Enter condition (or press Enter for no condition): ").strip() or "1=1"
            try:
                records = read_records(conn, table, condition)
                print("Records:")
                display_records(records)
            except Exception as e:
                print(f"Error reading records: {e}")
                
        elif command == "update":
            table = input("Enter table name to update record: ").strip()
            condition = input("Enter condition for records to update: ").strip()
            updates = {}
            col_names = input("Enter columns to update (comma separated): ").split(",")
            for col in col_names:
                col = col.strip()
                if col:
                    value = input(f"Enter new value for '{col}': ").strip()
                    updates[col] = value
            update_record(conn, table, updates, condition)
            
        elif command == "delete":
            table = input("Enter table name to delete records: ").strip()
            condition = input("Enter condition for records to delete: ").strip()
            delete_record(conn, table, condition)
            
        elif command == "exit":
            print("Exiting application.")
            break
            
        else:
            print("Invalid command. Please try again.")
    
    conn.close()

if __name__ == "__main__":
    main()
