"""Hashing and input checking module"""

import logging
import secrets
import sqlite3
import string


def generate_path():
    """ "Generate path value"""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(7))


def check_url_whitespace(url_input):
    """Perform checks to ensure input is in expected format"""
    for i in url_input:
        if i.isspace():
            logging.error("Whitespace in URL")
            return False
        logging.info("No whitespace in URL")
        return True


def check_url_security(url_input):
    """Perform checks to ensure input is in expected format"""
    if url_input[:5] == "https":
        logging.info("URL has TLS")
        return True
    logging.error("TLS not found")
    return False


def check_url_reputation(url_input):
    """Query badsites db for known bad reputation sites"""
    con = sqlite3.connect("badsites.db")
    cur = con.cursor()

    cur.execute("""SELECT * FROM badsites""")
    bad_sites = cur.fetchall()
    for site in bad_sites:
        if site[0] in url_input:
            logging.error("Bad reputation found for URL: %s", url_input)
            con.close()
            return False
    logging.info("No bad reputation found")
    con.close()
    return True
