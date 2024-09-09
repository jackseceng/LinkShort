# Test redis in k8s cluster from Linkshort container:
## Make a test entry
- Connect to terminal on the app container
- Start python:
```txt
root@LinkShort:/app# python
Python 3.12.4 (main, Aug  2 2024, 14:41:30) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
- Create a redis connection python object
```txt
import redis
r = redis.StrictRedis(host="redis-service", port=6379, db=0, charset="utf8", decode_responses=True)
```
- Set Key value pair:
```txt
r.set("jack", "edwards")
True
```
- Check that value is returned:
```txt
r.get("jack")
'edwards'
```
## Verify in REDIS DB
- Connect a terminal to the redis master
- Run test query:
```txt
get jack
"edwards"
```