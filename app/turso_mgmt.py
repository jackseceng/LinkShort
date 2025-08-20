"""Turso query and connection management module"""

import logging
from os import environ
from re import search

from dotenv import load_dotenv
from libsql import connect

load_dotenv()

url = environ["ENDPOINT"]
auth_token = environ["TOKEN"]


def _create_connection():
    """Creates and returns a new database connection."""
    conn = connect("urls.db", sync_url=url, auth_token=auth_token)
    conn.sync()
    return conn


def get_link(hashsum: str):
    """Get entries that match provided path, return output string or bool False if fail"""
    conn = _create_connection()
    try:
        result_set = conn.execute(
            "SELECT url, salt FROM urls WHERE hashsum = ?", (hashsum,)
        )
        row = result_set.fetchone()

        if row:
            # Ensure data is returned as bytes, adjust if your schema stores them differently
            url_data = (
                row[0] if isinstance(row[0], bytes) else bytes(str(row[0]), "utf-8")
            )
            salt_data = (
                row[1] if isinstance(row[1], bytes) else bytes(str(row[1]), "utf-8")
            )
            return url_data, salt_data
        return False, False
    except Exception as e:  # Use specific or general exception
        logging.error("Error on get_link: %s", e)
        return False, False
    finally:
        if conn:
            conn.close()


def insert_link(hashsum: str, url: bytes, salt: bytes):
    """Insert an entry under the specified path, return bool outcome"""
    unique_error = "UNIQUE constraint failed: urls.hashsum"
    conn = _create_connection()
    try:
        # Insert entry
        conn.execute(
            "INSERT INTO urls(hashsum, url, salt) VALUES (?, ?, ?);",
            (hashsum, url, salt),
        )
        conn.commit()
        return True, None
    except Exception as e:  # Changed from Error to a more general Exception
        if search(unique_error, str(e)):
            logging.warning("Entry already exists: %s", e)
            return False, "non-unique"
        logging.error("Error on insert_link: %s", e)
        return False, str(e)
    finally:
        if conn:
            conn.close()
