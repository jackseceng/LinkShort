import time
import redis
import logging


# Create redis connection object
r = redis.Redis(host="redis-master", port=6379, username="default", password="master-password", db=0)


def insert_link(path, link, max_retries=3):
    for attempt in range(max_retries):
        try:
            # Set a key-value pair
            r.set(path, link)
            r.close()
            return True

        except Exception as e:
            error = (f"Error: {e}")
            logging.warning(error)
            # Retry logic
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                logging.warning("Retry limit reached")
                r.close()
                return False


def get_link(path, max_retries=3):
    for attempt in range(max_retries):
        try:
            # Get the value for the key
            retrieved_value = r.get(path)
            r.close()
            return retrieved_value

        except Exception as e:
            error = (f"Error: {e}")
            logging.warning(error)
            # Retry logic
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                logging.warning("Retry limit reached")
                r.close()
                return False

        finally:
            # Close the Redis connection
            r.close()


def check_link(path, max_retries=3):
    for attempt in range(max_retries):
        try:
            # Check if the key exists
            if r.exists(path):
                return True
            else:
                return False

        except Exception as e:
            error = (f"Error: {e}")
            logging.warning(error)
            # Retry logic
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                logging.warning("Retry limit reached")
                return False

        finally:
            # Close the Redis connection
            r.close()
