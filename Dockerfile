FROM python:3.13.1-alpine3.21

COPY ./requirements.txt /tmp/requirements.txt

RUN set -e; \
        apk update && apk add --no-cache \
            openrc=0.55.1-r2 \
            gcc=14.2.0-r4 \
            curl=8.11.1-r0 \
            sqlite=3.47.1-r0 \
            libc-dev=1.2.5-r8 \
            linux-headers=6.6-r1 \
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
    CMD curl -f http://localhost:8080 || exit 1

# Switch to non-root user
USER appuser
EXPOSE 80
CMD ["gunicorn","--config", "gunicorn_cfg.py", "app:app"]