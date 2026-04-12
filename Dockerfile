# TEMPORARY: vulnerable test image - do not merge
FROM ubuntu:14.04

RUN apt-get update && apt-get install -y \
    busybox \
    openssl \
    curl

CMD ["busybox", "sh"]
