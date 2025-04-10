# Build in alpine python image
FROM python:3.13.2-alpine3.21 AS build-env

# Copy applicaiton files
WORKDIR /
COPY . .

# Install python dependencies, set up URL reputation DB
RUN set -e; \
    pip install --no-cache-dir -r requirements.txt --target /packages; \
    pip install --no-cache-dir urllib3==2.3.0; \
    python3 lists.py; \
    rm -rf requirements.txt; \
    rm -rf lists.py;

# Set runtime to distroless image
FROM python:3.13.2-alpine3.21
WORKDIR /app

# Copy packages and dependencies
COPY --from=build-env /lib/ld-musl-x86_64.so.1 /usr/lib/x86_64-linux-musl/libc.so
COPY --from=build-env /app /app
COPY --from=build-env /packages /packages

# Set up container healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
    CMD ["python", "healthcheck/healthcheck.py"]

# Run gunicorn process and expose port
ENV PYTHONPATH=/packages
EXPOSE 80
# Skipping user check as this is using a nonroot image
#checkov:skip=CKV_DOCKER_3:Ensure that a user for the container has been created
CMD ["python", "gunicorn_cfg.py"]