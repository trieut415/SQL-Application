# 🧠 Chat SQL Assistant

A command-line application that enables users to interact with an SQLite database using natural language. The assistant converts natural language queries to SQL using OpenAI's GPT model, while also supporting CRUD operations and CSV imports.

## 📦 Features

- 🔍 **Natural Language to SQL**: Translate user-friendly queries into SQL using OpenAI.
- 📊 **CSV Loader**: Import CSV files directly into the SQLite database.
- 🛠️ **CRUD Operations**: Create, read, update, and delete records with prompts.
- 🗃️ **Schema Awareness**: Auto-detect table schemas and assist during operations.
- 🧾 **Error Logging**: Centralized error logging with timestamps for easy debugging.

## 📁 Project Structure

```bash
SQL-Application/
├── chat_sql_assistant/          # 📦 Main package directory
│   ├── __init__.py              # Marks this folder as a Python package
│   ├── ai_assistant.py          # Converts natural language queries into SQL using OpenAI API
│   ├── crud.py                  # Performs Create, Read, Update, Delete operations on the database
│   ├── csv_loader.py            # Loads CSV files into SQLite, handles schema conflicts
│   ├── database.py              # Handles DB connection and query execution
│   ├── utils.py                 # Provides logging utility for error tracking
├── main.py                      # 🚀 Entry point for CLI — runs the full application
├── setup.py                     # 🛠 Python packaging script for pip installation
├── requirements.txt             # 📦 List of Python package dependencies
└── README.md                    # 📘 Project description and usage instructions

```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- OpenAI Python SDK (`pip install openai`)
- SQLite3
- Pandas (`pip install pandas`)

### Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/chat-sql-assistant.git
   cd chat-sql-assistant

2. Set your OpenAI API key:

```bash
export OPENAI_API_KEY="your-api-key"
```
3. Run the app:
```python
python3 main.py
```

## 💬 Commands
- load – Load a CSV file into the database

- query – Ask a natural language question

- list – List all tables

- create – Add a record to a table

- read – Read records with optional filtering

- update – Update record(s) with conditions

- delete – Delete record(s) based on condition

- exit – Close the application

## 📝 Example
```shell
> Enter command: query
> Enter your natural language query: show me the 5 most recent orders
```

Returns:
```sql
SQL Query: SELECT * FROM orders ORDER BY date DESC LIMIT 5;
```

Explanation: Retrieves the latest 5 orders sorted by date in descending order.

## Developer Notes
- All logs are written to error_log.txt.

- CSV import supports overwrite, rename, or skip options on schema conflict.

- AI prompt context includes full table schema for better SQL generation.
