"""Hashing and input checking module"""

import logging
from re import sub

from bcrypt import gensalt, hashpw


def generate_path(original_url):
    """Generate path path value"""
    hash_object = hashpw(original_url.encode(), gensalt(rounds=15))
    hash_string = sub(r"\W+", "", str(hash_object, encoding="utf-8"))
    # Return last 7 characters of resulting generated path
    return hash_string[-7:]


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
    logging.warning("Security not found")
    return False
