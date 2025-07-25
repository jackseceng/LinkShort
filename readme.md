# LinkShort - Containerised URL Shortener

Scans:

[![SCA](https://snyk.io/test/github/jackseceng/LinkShort/badge.svg)](https://snyk.io/test/github/jackseceng/LinkShort)
[![SAST](https://github.com/jackseceng/LinkShort/actions/workflows/codeql.yml/badge.svg)](https://codeql.github.com/)
[![Image](https://github.com/jackseceng/LinkShort/actions/workflows/container.yml/badge.svg)](https://github.com/jackseceng/LinkShort/actions/workflows/container.yml)
[![Linter](https://github.com/jackseceng/LinkShort/actions/workflows/lint.yml/badge.svg)](https://github.com/marketplace/actions/super-linter)

Size:

![Image Size](https://img.shields.io/docker/image-size/jackseceng/linkshort/latest)
![Codebase Size](https://img.shields.io/github/languages/code-size/jackseceng/LinkShort)

This is the Python code and Docker configuration for a link shortening web app

- Running demonstration available at [cubel.ink](https://cubel.ink)

- [DockerHub image repository](https://hub.docker.com/r/jackseceng/linkshort)

I am using this to learn:
- Docker & Web App Hosting
- Python Development
- DevSecOps Automation

## Testing locally

- [Sign up for a free Turso account](https://app.turso.tech/signup), and create database with a table called 'urls' in with the follwing SQL statement:
```SQL
CREATE TABLE
  urls (
    hashsum VARCHAR(64) PRIMARY KEY,
    url BLOB,
    salt BLOB,
    CONSTRAINT unique_hash UNIQUE (hashsum)
  );
```


- Create a file in the `/app` directory called `.env`, with the following contents, setting the appropriate values with your own substitutions:
```txt
ENDPOINT="<your-turso-url>"
TOKEN="<your-turso-token>"
TLD=localhost
```

**! WARNING !**

Please make sure your local environment variables in your terminal do not share names with the ones in this `.env` file.
> If you change the names of the variables in this file, make sure to change their references in the `docker-compose.yaml` file as well.

### Docker compose
From the root directory of this repository, run:
```bash
docker compose up -d --build
```
```bash
[+] Running (2/2)
 ✔ Network linkshort_ls-net   Created
 ✔ Container linkshort-app-1  Started
```

If succesful, app will be running at [http://localhost](http://localhost), it will connect to your Turso database over the internet.

You can re-run this command whenever you make changes to rebuild the container.

To shut down the service, run this command:
```bash
docker compose down
```

## Application Features

- [x] Shortens URLs with unique extensions
- [x] Encrypts stored URLs along with random with salts
- [x] Extensions are stored as hashsums in the DB
- [x] Sanitisation of input from user for both URLs and extensions on requests
- [x] Checks on user shared URLs, to ensure they begin with HTTPS
- [x] Uses minimal scratch image for runtime security
- [x] Checks submitted URLs against spam lists, rejects known spam domains
- [x] Generates QR codes for users to download and share
- [x] A frontend with reactive CSS & HTML
- [x] 400 and 500 HTTP error handling with pages
- [x] Static content served through CDN

> This has been set up via [statically.io](https://statically.io/)

- [x] Demonstration application set up:

> This has been set up on [cloud.run](https://cloud.run) via it's repository integration

## DevSecOps Automation

Code Linting:
- [x] [Super Linter](https://github.com/super-linter/super-linter)

Static & Software Composition Analysis:
- [x] [CodeQL](https://codeql.github.com/)
- [x] [Snyk](https://snyk.io)

Container Image Scanning:
- [x] [Grype](https://github.com/anchore/grype/)
- [x] [Docker Scout](https://docs.docker.com/scout/)
- [x] [Trivy](https://trivy.dev/latest/docs/target/container_image/)

Automated Dependency Upgrades:
- [x] [Renovate](https://www.mend.io/free-developer-tools/renovate/)

Commit Standardisation:
- [x] [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) Commit title standardisation

## Developed by [Jack](https://jacksec.engineer)
