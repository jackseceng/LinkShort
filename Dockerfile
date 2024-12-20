FROM python:3.13.1-alpine3.21

COPY ./requirements.txt /tmp/requirements.txt

RUN set -e; \
        apk update && apk add --no-cache \
            openrc \
            gcc \
            curl \
            sqlite \
            gcc \
            libc-dev \
            linux-headers \
    ; \
    pip install --no-cache-dir -r /tmp/requirements.txt;

# Create a non-root user and group
RUN addgroup -S appuser && adduser -S -G appuser appuser

COPY . /app
COPY .env /app/src

WORKDIR /app/src

# Set up permissions
RUN chown -R appuser:appuser /app/src

# Container Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
    CMD curl -f http://localhost || exit 1

# Switch to non-root user
USER appuser
EXPOSE 80
CMD ["gunicorn","--config", "gunicorn_config.py", "app:app"]