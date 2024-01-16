FROM python:3.12.0a1-slim
COPY /src /home/app
WORKDIR /home/app
RUN apt-get update --fix-missing && \
    apt-get -y install libpq-dev gcc && \
    groupadd --gid 1000 app && \
    useradd --gid 1000 --uid 1000 app && \
    mkdir -p /home/app/src && \
    pip3 install --no-cache-dir --upgrade pip -r requirements.txt && \
    chown -R app:app /home/app
USER app

# Prod run command
# EXPOSE 80
# EXPOSE 6379
# CMD [ "python3", "app.py" ]

# Dev run command
EXPOSE 5000
EXPOSE 6379
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "-p 5000" ]