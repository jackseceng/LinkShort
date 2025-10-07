"""Hashing and input checking module"""

import base64
import logging
import secrets
import string

import requests
import urllib3
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

KDF_ALGORITHM = hashes.SHA256()
KDF_LENGTH = 32
KDF_ITERATIONS = 120000


def generate_path():
    """ "Generate path value"""
    try:
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(7))
    except Exception as e:
        logging.error("Error on generate_path: %s", e)
        return False


def encrypt_url(url: str, linkpath: str):
    """Derive a symmetric key using the path and a random salt."""
    try:
        salt = secrets.token_bytes(16)
        kdf = PBKDF2HMAC(
            algorithm=KDF_ALGORITHM,
            length=KDF_LENGTH,
            salt=salt,
            iterations=KDF_ITERATIONS,
        )
        key = kdf.derive(linkpath.encode("utf-8"))

        # Encrypt the message.
        f = Fernet(base64.urlsafe_b64encode(key))
        ciphertext = f.encrypt(url.encode("utf-8"))

        return ciphertext, salt
    except Exception as e:
        logging.error("Error on encrypt_url: %s", e)
        return False, False


def decrypt_url(ciphertext: bytes, linkpath: str, salt: bytes):
    """Decrypt URL using extension from user request and salt from database"""
    try:
        kdf = PBKDF2HMAC(
            algorithm=KDF_ALGORITHM,
            length=KDF_LENGTH,
            salt=salt,
            iterations=KDF_ITERATIONS,
        )
        key = kdf.derive(linkpath.encode("utf-8"))

        # Decrypt the message
        f = Fernet(base64.urlsafe_b64encode(key))
        plaintext = f.decrypt(ciphertext)

        return plaintext
    except Exception as e:
        logging.error("Error on decrypt_url: %s", e)
        return False


def check_url_whitespace(url_input):
    """Perform checks to ensure input is in expected format"""
    try:
        for i in url_input:
            if i.isspace():
                return False
            return True
    except Exception as e:
        logging.error("Error on check_url_whitespace: %s", e)
        return False


def check_url_security(url_input):
    """Perform checks to ensure input is in expected format"""
    try:
        if url_input[:5] == "https":
            return True
        return False
    except Exception as e:
        logging.error("Error on check_url_security: %s", e)
        return False


def check_url_reputation(url_input):
    """Compile list of bad sites, and compare to input"""
    try:
        with urllib3.PoolManager() as http:
            URL1 = "https://raw.githubusercontent.com/Spam404/lists/master/main-blacklist.txt"
            URL2 = "https://raw.githubusercontent.com/stamparm/blackbook/refs/heads/master/blackbook.txt"

            response1 = http.request("GET", URL1)
            response2 = http.request("GET", URL2)

            text1 = response1.data.decode("utf-8")
            text2 = response2.data.decode("utf-8")

            blacklist = text1 + text2

            for line in blacklist.splitlines():
                if line and line in url_input:
                    return False
        return True
    except Exception as e:
        logging.error("Error on check_url_reputation: %s", e)
        return False


def validate_turnstile(token, secret, remoteip=None):
    url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"

    data = {"secret": secret, "response": token}

    if remoteip:
        data["remoteip"] = remoteip

    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Turnstile validation error: {e}")
        return {"success": False, "error-codes": ["internal-error"]}
