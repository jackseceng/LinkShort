import time
from rediscluster import RedisCluster

# Test this using a python container in the same docker network as the redis cluster defined in the docker-compose file (ls-net)

def get_redis_connection():
    # Update with your Redis Sentinel service or container names
    startup_nodes = [
        {"host": "sentinel-0"},
        {"host": "sentinel-1"},
        {"host": "sentinel-2"}
    ]

    # Create a RedisCluster instance
    redis_cluster = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

    return redis_cluster


def insert_link(path, link, max_retries=3, retry_delay=1):
    for attempt in range(max_retries):
        try:
            # Connect to the Redis cluster
            redis_connection = get_redis_connection()

            # Check if the key already exists
            if redis_connection.exists(path):
                # Cancel operation if it already exists
                print(f"Key '{path}' already exists. Skipping set operation.")
            else:
                # Set a key-value pair
                redis_connection.set(path, link)
                print(f"Value inserted for key: '{path}': {link}")

        except Exception as e:
            print(f"Error: {e}")
            # Retry logic
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Operation failed.")

        finally:
            # Close the Redis connection
            redis_connection.close()


def get_link(path, max_retries=3, retry_delay=1):
     for attempt in range(max_retries):
        try:
            # Connect to the Redis cluster
            redis_connection = get_redis_connection()

            # Get the value for the key
            retrieved_value = redis_connection.get(path)

            print(f"Retrieved value for key '{path}': {retrieved_value}")

        except Exception as e:
            print(f"Error: {e}")
            # Retry logic
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Operation failed.")

        finally:
            # Close the Redis connection
            redis_connection.close()
