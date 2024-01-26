"""Redis query and connection management module"""
import time
import logging
import redis


# Create redis connection object
r = redis.StrictRedis(
    host="redis-master",
    port=6379,
    username="default",
    password="master-password", 
    db=0,
    charset="utf8",
    decode_responses=True
)


def insert_link(path, link, max_retries=3):
    """Insert path and generated link into redis"""
    for attempt in range(max_retries):
        try:
            # Set the key-value pair
            r.set(path, link)
            r.close()
            return True
        except redis.exceptions.RedisError as e:
            # Log redis error to console
            error = f"Error: {e}"
            logging.warning(error)
            # Redis retry logic
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                logging.warning("Redis retry limit reached")
                r.close()
                return False


def get_link(path, max_retries=3):
    """Get original link with path from redis"""
    for attempt in range(max_retries):
        try:
            # Get the value for given key
            retrieved_value = r.get(path)
            r.close()
            return retrieved_value
        except redis.exceptions.RedisError as e:
            # Log redis error to console
            error = f"Error: {e}"
            logging.warning(error)
            # Retry logic
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                logging.warning("Retry limit reached")
                r.close()
                return False


def check_link(path, max_retries=3):
    """Check for path collision in redis"""
    for attempt in range(max_retries):
        try:
            # Check if the key exists
            if r.exists(path):
                return True
            else:
                return False
        except redis.exceptions.RedisError as e:
            # Log redis error to console
            error = f"Error: {e}"
            logging.warning(error)
            # Retry logic
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                logging.warning("Retry limit reached")
                r.close()
                return False
