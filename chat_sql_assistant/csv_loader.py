import os
import pandas as pd
from chat_sql_assistant.utils import log_error
from chat_sql_assistant.database import execute_query

def handle_schema_conflict(table_name, conn):
    """
    Handle schema conflicts for an existing table.
    Prompts the user to either overwrite, rename, or skip the CSV load.
    """
    cursor = execute_query(conn, f"PRAGMA table_info({table_name})")
    existing_schema = cursor.fetchall()
    print(f"Existing schema for '{table_name}': {existing_schema}")
    
    decision = input(f"Table '{table_name}' exists. Choose action - Overwrite (O), Rename (R), or Skip (S): ").upper()
    if decision == 'O':
        execute_query(conn, f"DROP TABLE IF EXISTS {table_name}")
        print(f"Table '{table_name}' dropped. Proceeding with creation.")
    elif decision == 'R':
        new_name = input("Enter new table name: ")
        print(f"Table will be created with the name '{new_name}'.")
        table_name = new_name
    elif decision == 'S':
        print(f"Skipping CSV load for table '{table_name}'.")
        raise Exception("CSV load skipped by user decision.")
    else:
        print("Invalid option. Skipping CSV load.")
        raise Exception("Invalid user option for schema conflict.")
    return table_name

def create_table_from_csv(csv_path, conn, table_name=None):
    """
    Create a table from a CSV file by inferring the schema and inserting data.
    """
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        log_error(f"Error reading CSV file '{csv_path}': {e}")
        raise Exception(f"Error reading CSV: {e}")
    
    if not table_name:
        table_name = os.path.splitext(os.path.basename(csv_path))[0]
    
    # Check if table exists
    existing_tables = [row[0] for row in execute_query(conn, "SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    if table_name in existing_tables:
        try:
            table_name = handle_schema_conflict(table_name, conn)
        except Exception as e:
            log_error(f"Schema conflict handling error for table '{table_name}': {e}")
            raise

    # Map pandas dtypes to SQLite types
    type_map = {'object': 'TEXT', 'int64': 'INTEGER', 'float64': 'REAL'}
    schema_parts = []
    for col, dtype in zip(df.columns, df.dtypes.astype(str)):
        sql_type = type_map.get(dtype, 'TEXT')
        schema_parts.append(f'"{col}" {sql_type}')
    
    create_stmt = f"CREATE TABLE {table_name} ({', '.join(schema_parts)})"
    try:
        execute_query(conn, create_stmt)
        # Insert data into the new table
        df.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"Table '{table_name}' created and CSV data inserted successfully.")
    except Exception as e:
        log_error(f"Error creating table '{table_name}': {e}")
        raise Exception(f"Error creating table: {e}")
