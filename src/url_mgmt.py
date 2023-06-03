"""Modules: MD5 hashing function, regex sub function"""
from hashlib import sha256
from re import sub


def generate_path(og_url):
    """Generate path URN value"""
    hash_object = sha256(og_url.encode()).hexdigest()  # Hash original URL into MD5
    path_id = sub('[^0-9]', '', hash_object)  # Extract all numeric characters from hashsum
    return int(path_id[:7])  # Return first 7 characters of resulting generated path


def check_url(url_input, check_type):
    """Perform checks to ensure input is in expected format"""
    match check_type:
        case 1:
            # whitespace check
            for i in url_input:
                if i.isspace():
                    return False
        case 2:
            # protocol check
            return url_input[:8] == 'https://'  # Check that URL begins with https
        case 3:
            # string check
            if len(url_input) > 7:  # Check that URN provided has 7 characters or fewer
                return False  # False if length check fails
            for i in url_input:
                if not i.isnumeric():
                    return False  # False if numeric check fails
            return True  # Return true if all checks pass
        case _:
            return False
            # Catch all case for any URNs that do not explicitly pass all checks, return false
