import openai
from database import execute_query
from utils import log_error

def generate_sql_from_nl(nl_query, conn):
    """
    Convert a natural language query into an SQL query using OpenAI.
    Gathers the current table schemas and sends a prompt to the API.
    """
    try:
        cursor = execute_query(conn, "SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        schema_info = ""
        for (table,) in tables:
            cursor = execute_query(conn, f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            col_names = [col[1] for col in columns]
            schema_info += f"Table {table}: " + ", ".join(col_names) + "\n"
        
        prompt = f"""You are an AI assistant tasked with converting user queries into SQL statements.
The database uses SQLite and contains the following tables:
{schema_info}
User Query: "{nl_query}"
Please provide:
- SQL Query: (the SQL query to answer the request)
- Explanation: (a short comment explaining what the query does)
"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        content = response['choices'][0]['message']['content']
        # Basic parsing: extract lines beginning with "SQL Query:" and "Explanation:"
        sql_query, explanation = None, None
        for line in content.splitlines():
            if line.startswith("SQL Query:"):
                sql_query = line.replace("SQL Query:", "").strip()
            elif line.startswith("Explanation:"):
                explanation = line.replace("Explanation:", "").strip()
        return sql_query, explanation
    except Exception as e:
        log_error(f"Error generating SQL from natural language: {e}")
        raise Exception(f"Error generating SQL: {e}")
