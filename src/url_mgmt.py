"""Modules: MD5 hashing function, regex sub function"""
import bcrypt

import logging

from re import sub


def generate_path(og_url):
    """Generate path path value"""
    logging.warning("Generating path function")
    hash_object = bcrypt.hashpw(og_url.encode(), bcrypt.gensalt(rounds=15))
    logging.warning("Hash object generated")
    hash_string = sub(r'\W+', '', str(hash_object, encoding='utf-8'))
    logging.warning("Hash string generated")
    logging.warning(hash_string[:7])
    return hash_string[:7]  # Return first 7 characters of resulting generated path


def check_url(url_input, check_type):
    """Perform checks to ensure input is in expected format"""
    logging.warning("Checking URL")
    match check_type:
        case 1:
            logging.warning("Checking for whitespace")
            # whitespace check
            for i in url_input:
                if i.isspace():
                    return False
        case 2:
            logging.warning("Checking for https")
            # protocol check
            return url_input[:8] == 'https://'  # Check that URL begins with https
        case 3:
            logging.warning("Checking path length")
            # length check
            if len(url_input) != 7:  # Check if path is exactly 7 characters
                return False  # False if length check fails
            return True  # Return true if all checks passes
        case _:
            logging.warning("Catch all URL check")
            return False
            # Catch all case for any URNs that do not explicitly pass all checks, return false
