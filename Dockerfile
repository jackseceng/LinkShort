FROM python:3.12.6-slim-bookworm

RUN apt-get update && apt-get install --no-install-recommends -y nginx=1.22.1-9 gcc=4:12.2.0-3 libc6-dev=2.36-9+deb12u8 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user and group
RUN groupadd -r appuser && useradd -r -g appuser -s /sbin/nologin -d /app appuser

WORKDIR /app

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

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

# Switch to non-root user
USER appuser

CMD ["./start.sh"]
EXPOSE 80
