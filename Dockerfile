FROM python:3.13.1-alpine3.21

COPY ./requirements.txt /tmp/requirements.txt

RUN set -e; \
        # Install OS dependencies
        apk update && apk add --no-cache \
            curl=8.11.1-r0 \
    ; \
    # Install python requirements then remove requirements file
    pip install --no-cache-dir -r /tmp/requirements.txt; \
    rm -rf /tmp; \
    # Create a non-root user and group
    addgroup -S appuser && adduser -S -G appuser appuser;

# Copy in application files
WORKDIR /app
COPY app/ .

# Give appuser permissions for app directory
RUN chown -R appuser:appuser /app

# Container Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080 || exit 1

# Switch to non-root user
USER appuser
EXPOSE 80
CMD ["gunicorn","--config", "gunicorn_cfg.py", "app:app"]
