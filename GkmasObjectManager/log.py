"""
log.py
Console logger.
"""


class Logger(Console):
    """
    A console logger with custom log levels.

    Methods:
        info(message: str): Logs an informational message in white text.
        success(message: str): Logs a success message in green text.
        warning(message: str): Logs a warning message in yellow text.
        error(message: str): Logs an error message in red text
            followed by traceback, and raises an error.
    """

    def __init__(self):
        super().__init__()

    def info(self, message: str):
        print(f"[Info] {message}")

    def success(self, message: str):
        print(f"[Success] {message}")

    def warning(self, message: str):
        print(f"[Warning] {message}")

    def error(self, message: str):
        print(f"[Error] {message}")
        raise
