"""Hashing and input checking module"""

import logging
import string
import secrets


def generate_path():
    """ "Generate path value"""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(7))


def check_url_whitespace(url_input):
    """Perform checks to ensure input is in expected format"""
    for i in url_input:
        if i.isspace():
            logging.error("Whitespace found")
            return False
        logging.info("Whitespace not found")
        return True


def check_url_security(url_input):
    """Perform checks to ensure input is in expected format"""
    if url_input[:5] == "https":
        logging.info("Security found")
        return True
    logging.error("Security not found")
    return False
