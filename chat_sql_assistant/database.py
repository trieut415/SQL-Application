import sqlite3
from chat_sql_assistant.utils import log_error

def connect_db(db_path="data.db"):
    """Connect to SQLite database."""
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        log_error(f"Database connection error: {e}")
        raise

def execute_query(conn, query, params=None):
    """Execute an SQL query with optional parameters and commit the transaction."""
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return cursor
    except sqlite3.Error as e:
        log_error(f"Error executing query '{query}': {e}")
        raise

def get_tables(conn):
    """Return a list of table names in the database."""
    try:
        cursor = execute_query(conn, "SELECT name FROM sqlite_master WHERE type='table'")
        return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        log_error(f"Error retrieving tables: {e}")
        return []
