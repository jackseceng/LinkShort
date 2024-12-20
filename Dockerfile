FROM python:3.13.1-alpine3.21

WORKDIR /app

COPY ./requirements.txt /tmp/requirements.txt

RUN set -e; \
        apk update && apk add --no-cache \
            openrc \
            nginx \
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

COPY ./app .
COPY .env .
COPY start.sh /app/
COPY nginx.conf /etc/nginx

# Set up permissions
RUN chmod +x ./start.sh && \
    chown -R appuser:appuser /app && \
    # Nginx needs these directories to be writable
    mkdir -p /var/log/nginx /var/lib/nginx && \
    chown -R appuser:appuser /var/log/nginx && \
    chown -R appuser:appuser /var/lib/nginx && \
    # Make nginx.conf readable by appuser
    chmod 644 /etc/nginx/nginx.conf

# Container Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080 || exit 1

# Switch to non-root user
USER appuser
CMD ["./start.sh"]
EXPOSE 80