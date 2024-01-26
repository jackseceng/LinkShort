"""Hashing and input checking module"""
import logging
from re import sub
import bcrypt


def generate_path(original_url):
    """Generate path path value"""
    hash_object = bcrypt.hashpw(original_url.encode(), bcrypt.gensalt(rounds=15))
    hash_string = sub(r'\W+', '', str(hash_object, encoding='utf-8'))
    # Return first 7 characters of resulting generated path
    return hash_string[:7]


def check_url_whitespace(url_input):
    """Perform checks to ensure input is in expected format"""
    logging.warning("URL Whitespace check")
    for i in url_input:
        if i.isspace():
            logging.warning("Whitespace found")
            return False
        logging.warning("Whitespace not found")
        return True

def check_url_security(url_input):
    """Perform checks to ensure input is in expected format"""
    logging.warning("URL Security check")
    if url_input[:5] is 'https':
        logging.warning("Security found")
        return True
    logging.warning("Security not found")
    return False
