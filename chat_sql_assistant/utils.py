import datetime

def log_error(error_message, file_name="error_log.txt"):
    """Append error message with timestamp to the error log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_name, "a") as f:
        f.write(f"[{timestamp}] {error_message}\n")
