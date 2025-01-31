FROM python:3.13.1-alpine3.21

# Copy applicaiton files
WORKDIR /
COPY . .

# Install dependencies
RUN set -e; \
        apk update && apk add --no-cache \
            curl=8.11.1-r0 \
    ; \
    pip install --no-cache-dir -r requirements.txt; \
    rm -rf requirements.txt;

# Create a non-root user and group
RUN addgroup -S appuser && adduser -S -G appuser appuser

# Create app directory and set permisisons
WORKDIR /app
RUN chown -R appuser:appuser /app

# Container Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080 || exit 1

# Switch to non-root user
USER appuser
EXPOSE 80
CMD ["gunicorn","--config", "gunicorn_cfg.py", "app:app"]
