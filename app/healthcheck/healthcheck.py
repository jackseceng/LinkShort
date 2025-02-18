#!/usr/bin/env python3
import sys

import requests


def check_health():
    try:
        response = requests.get("http://localhost:8080", timeout=3)
        if response.status_code == 200:
            sys.exit(0)  # Success
        else:
            sys.exit(1)  # Failure
    except requests.RequestException:
        sys.exit(1)  # Failure on connection error, timeout, etc.


if __name__ == "__main__":
    check_health()
