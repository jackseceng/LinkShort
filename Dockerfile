# Stage 1: Build stage environment using alpine python Image
FROM python:3.14.1-alpine3.21 AS build-env

# Set build directory
WORKDIR /build

# Copy application files
COPY . .

# Install python dependencies into a target directory
RUN set -e; \
    apk add --no-cache \
    build-base=0.5-r3 \
    cmake=3.31.1-r0 \
    coreutils=9.5-r2; \
    pip install --no-cache-dir -r requirements.txt --target /packages;


# Stage 2: Runtime Stage using scratch Image
FROM scratch

# Copy necessary system libraries and interpreter from build-env
COPY --from=build-env /lib/ld-musl-x86_64.so.1 /lib/ld-musl-x86_64.so.1
COPY --from=build-env /lib/libc.musl-x86_64.so.1 /lib/libc.musl-x86_64.so.1
COPY --from=build-env /usr/local/lib/libpython3.14.so.1.0 /usr/local/lib/libpython3.14.so.1.0
COPY --from=build-env /usr/local/lib/python3.14 /usr/local/lib/python3.14
COPY --from=build-env /usr/lib/libssl.so.3 /usr/lib/libssl.so.3
COPY --from=build-env /usr/lib/libcrypto.so.3 /usr/lib/libcrypto.so.3
COPY --from=build-env /usr/lib/libz.so.1 /usr/lib/libz.so.1
COPY --from=build-env /usr/lib/libgcc_s.so.1 /usr/lib/libgcc_s.so.1

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

# Set runtime directory
WORKDIR /app

# Expose the application port
EXPOSE 80

# Set up container healthcheck 
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
    CMD ["/usr/local/bin/python", "healthcheck/healthcheck.py"]

# Define the command to run the application
CMD ["/usr/local/bin/python", "gunicorn_cfg.py"]
