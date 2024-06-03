# Test redis in k8s cluster from Linkshort container:
- First connect to terminal on Linkshort container, then:

# Create redis connection object:
import redis
r = redis.StrictRedis(host="redis-service", port=6379, db=0, charset="utf8", decode_responses=True)

# Set Key value pair:
r.set("jack", "edwards")
True

# Check that value is returned:
r.get("jack")
'edwards'

# Verify on redis container:
- Connect to terminal on redis container, then:
get jack
"edwards"