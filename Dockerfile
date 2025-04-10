# Stage 1: Build environment using Alpine Python
FROM python:3.13.3-alpine3.21 AS build-env

# Set working directory
WORKDIR /build

# Copy application files
COPY requirements.txt .

# Install python dependencies into a target directory
RUN set -e; \
    pip install --no-cache-dir -r requirements.txt --target /packages; \
    pip install --no-cache-dir urllib3==2.3.0

# Copy the rest of the application code
COPY . .

# Run build-time script for bad sites db creation and clean up
RUN set -e; \
    python3 lists.py; \
    rm -rf requirements.txt; \
    rm -rf lists.py;

# Stage 2: Runtime Stage based on scratch as minimal runtime container
FROM scratch

# Copy necessary system libraries and interpreter from build-env
COPY --from=build-env /lib/ld-musl-x86_64.so.1 /lib/ld-musl-x86_64.so.1
COPY --from=build-env /lib/libc.musl-x86_64.so.1 /lib/libc.musl-x86_64.so.1
COPY --from=build-env /usr/local/lib/libpython3.13.so.1.0 /usr/local/lib/libpython3.13.so.1.0
COPY --from=build-env /usr/local/lib/python3.13 /usr/local/lib/python3.13
COPY --from=build-env /usr/lib/libssl.so.3 /usr/lib/libssl.so.3
COPY --from=build-env /usr/lib/libcrypto.so.3 /usr/lib/libcrypto.so.3
COPY --from=build-env /usr/lib/libz.so.1 /usr/lib/libz.so.1
COPY --from=build-env /usr/lib/libsqlite3.so.0 /usr/lib/libsqlite3.so.0

# Copy Python installation
COPY --from=build-env /usr/local/bin/python /usr/local/bin/python

# Copy CA certificates needed for SSL verification
COPY --from=build-env /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

# Copy installed packages
COPY --from=build-env /packages /packages

# Copy application code
COPY --from=build-env /build/app /app

# Set required environment variables for Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    PYTHONPATH=/packages \
    SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

# Set working directory
WORKDIR /app

# Expose the application port
EXPOSE 80

# Set up container healthcheck 
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
    CMD ["/usr/local/bin/python", "healthcheck/healthcheck.py"]

# Define the command to run the application, skip check as scrach can't have users
#checkov:skip=CKV_DOCKER_3:Ensure that a user for the container has been created
CMD ["/usr/local/bin/python", "gunicorn_cfg.py"]
