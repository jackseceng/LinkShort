"""Turso query and connection management module"""

import logging
from os import environ

from dotenv import load_dotenv
from libsql import connect

load_dotenv()

url = environ["ENDPOINT"]
auth_token = environ["TOKEN"]

conn = connect(
    "urls.db", 
    sync_url=url, 
    auth_token=auth_token
)

conn.sync()


def get_link(hashsum: str):
    """Get entries that match provided path, return output string or bool False if fail"""
    try:
        result_set = conn.execute("SELECT url, salt FROM urls WHERE hashsum = ?", (hashsum,))
        row = result_set.fetchone()

        if row:
            # Ensure data is returned as bytes, adjust if your schema stores them differently
            url_data = row[0] if isinstance(row[0], bytes) else bytes(str(row[0]), 'utf-8')
            salt_data = row[1] if isinstance(row[1], bytes) else bytes(str(row[1]), 'utf-8')
            return url_data, salt_data
        return None, None # Or return False as per original logic for "not found"
    except Exception as e: # Use specific or general exception
        logging.error("Error on get_link: %s", e)
        return False


def insert_link(hashsum: str, url: bytes, salt: bytes):
    """Insert an entry under the specified path, return bool outcome"""
    try:
        with Session(engine) as session:
            # Insert entry
            new_entry = Entry(hashsum=str(hashsum), url=bytes(url), salt=bytes(salt))
            session.add(new_entry)
            session.commit()
            return True
    except Error as e:
        logging.error("Error on insert_link:  %s", e)
        return False


def check_link(hashsum: str):
    """Return if an entry exists under specified path"""
    try:
        result_set = conn.execute("SELECT 1 FROM urls WHERE hashsum = ?", (hashsum,))
        return result_set is not None
    except Exception as e:
        logging.error("Error on check_link:  %s", e)
        return False
