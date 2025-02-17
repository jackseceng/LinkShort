FROM python:3.13.2-alpine3.21 as build-env

# Copy applicaiton files
WORKDIR /
COPY . .

# Install dependencies
RUN set -e; \
        apk update && apk add --no-cache \
            curl \
    ; \
    pip install --no-cache-dir -r requirements.txt --target /packages; \
    rm -rf requirements.txt;

# Set up distroless container for runtime
FROM gcr.io/distroless/python3:nonroot
WORKDIR /app
COPY --from=build-env /app /app
COPY --from=build-env /packages /packages

# Container Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080 || exit 1

# Run process
ENV PYTHONPATH=/packages
EXPOSE 80
#checkov:skip=CKV_DOCKER_3:Ensure that a user for the container has been created
CMD ["gunicorn_cfg.py"]
