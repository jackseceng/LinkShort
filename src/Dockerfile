FROM python:3.12.4

RUN apt-get update && apt-get install --no-install-recommends -y nginx=1.22.1-9 iputils-ping redis-tools\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./app .
COPY .env .
COPY start.sh /app/
COPY nginx.conf /etc/nginx
RUN chmod +x ./start.sh

CMD ["./start.sh"]
EXPOSE 80
