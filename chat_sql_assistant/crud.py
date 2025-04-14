from chat_sql_assistant.database import execute_query
from chat_sql_assistant.utils import log_error

def create_record(conn, table, data):
    """
    Insert a new record into the specified table.
    'data' should be a dictionary of {column: value}.
    """
    try:
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        execute_query(conn, query, list(data.values()))
        print("Record inserted successfully.")
    except Exception as e:
        log_error(f"Error inserting record into {table}: {e}")
        print(f"Error inserting record: {e}")

def read_records(conn, table, condition="1=1", limit=10):
    """
    Read records from the specified table using an optional condition.
    """
    try:
        query = f"SELECT * FROM {table} WHERE {condition} LIMIT {limit}"
        cursor = execute_query(conn, query)
        records = cursor.fetchall()
        return records
    except Exception as e:
        log_error(f"Error reading records from {table}: {e}")
        print(f"Error reading records: {e}")
        return []

def update_record(conn, table, updates, condition):
    """
    Update records in the specified table.
    'updates' is a dictionary of {column: value} for the SET clause.
    'condition' is an SQL condition for the WHERE clause.
    """
    try:
        set_clause = ", ".join([f"{col}=?" for col in updates.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        execute_query(conn, query, list(updates.values()))
        print("Record(s) updated successfully.")
    except Exception as e:
        log_error(f"Error updating record in {table}: {e}")
        print(f"Error updating record: {e}")

def delete_record(conn, table, condition):
    """
    Delete records from the specified table using a condition.
    """
    try:
        query = f"DELETE FROM {table} WHERE {condition}"
        execute_query(conn, query)
        print("Record(s) deleted successfully.")
    except Exception as e:
        log_error(f"Error deleting record from {table}: {e}")
        print(f"Error deleting record: {e}")
