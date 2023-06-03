FROM python:3.12.0a1-slim
COPY /src /home/app
WORKDIR /home/app
RUN groupadd --gid 1000 app && \
    useradd --gid 1000 --uid 1000 app && \
    mkdir -p /home/app/src && \
    pip3 install --no-cache-dir --upgrade pip -r requirements.txt && \
    chown -R app:app /home/app
USER app
RUN chmod 664 links.sqlite
EXPOSE 80
ENTRYPOINT [ "gunicorn" ]
CMD [ "-b", "0.0.0.0:80", "app:app" ]