#!/usr/bin/env python3
import logging
import re
import os
import mysql.connector
from typing import List

# Define PII_FIELDS at the root of the module
PII_FIELDS = ("name", "email", "phone", "ssn", "password")

def filter_datum(fields, redaction, message, separator):
    """Function to obfuscate PII data in log messages."""
    pattern = f"({'|'.join(fields)})=([^\\{separator}]+)"
    return re.sub(pattern, lambda match: f"{match.group(1)}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        original_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, original_message, self.SEPARATOR)


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the database using environment variables for credentials."""
    db_username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    )


def get_logger() -> logging.Logger:
    """Function to create a logger for 'user_data' with a RedactingFormatter."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    return logger


def main() -> None:
    """Main function to retrieve and display data from the 'users' table."""
    db = get_db()  # Get the database connection
    cursor = db.cursor()

    query = "SELECT name, email, phone, ssn, password, ip, last_login, user_agent FROM users"
    cursor.execute(query)

    logger = get_logger()  # Set up the logger with RedactingFormatter

    for row in cursor.fetchall():
        name, email, phone, ssn, password, ip, last_login, user_agent = row
        message = f"name={name}; email={email}; phone={phone}; ssn={ssn}; password={password}; ip={ip}; last_login={last_login}; user_agent={user_agent};"
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
