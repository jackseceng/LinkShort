FROM python:3.12.0a1-slim
COPY /src /home/app
WORKDIR /home/app
RUN apt-get update && \
    apt-get -y install libpq-dev gcc redis-server && \
    groupadd --gid 1000 app && \
    useradd --gid 1000 --uid 1000 app && \
    mkdir -p /home/app/src && \
    pip3 install --no-cache-dir --upgrade pip -r requirements.txt && \
    chown -R app:app /home/app
USER app
# Gunicorn config for production
# EXPOSE 80
# ENTRYPOINT [ "gunicorn" ]
# CMD [ "-b", "0.0.0.0:80", "app:app", "--log-level debug" ]

# Flask config for debug
EXPOSE 5000
EXPOSE 6379
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "-p 5000"]