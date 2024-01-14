import time
import redis


# Create redis connection object
r = redis.Redis(host="redis-master", port=6379, username="default", password="master-password", db=0)


def insert_link(path, link, max_retries=3):
    for attempt in range(max_retries):
        try:
            # Check if the key already exists
            if r.exists(path):
                # Cancel operation if it already exists
                print(f"Key '{path}' already exists. Skipping set operation.")
                break
            else:
                # Set a key-value pair
                r.set(path, link)
                print(f"Value inserted for key: '{path}': {link}")
                break

        except Exception as e:
            print(f"Error: {e}")
            # Retry logic
            if attempt < max_retries - 1:
                print("Retrying in 1 seconds...")
                time.sleep(1)
            else:
                print("Max retries reached. Operation failed.")

        finally:
            # Close the Redis connection
            r.close()


def get_link(path, max_retries=3):
    for attempt in range(max_retries):
        try:
            # Get the value for the key
            retrieved_value = r.get(path)
            print(f"Retrieved value for key '{path}': {retrieved_value}")
            return retrieved_value

        except Exception as e:
            print(f"Error: {e}")
            # Retry logic
            if attempt < max_retries - 1:
                print("Retrying in 1 seconds...")
                time.sleep(1)
            else:
                print("Max retries reached. Operation failed.")

        finally:
            # Close the Redis connection
            r.close()
