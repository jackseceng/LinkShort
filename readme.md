[![Known Vulnerabilities](https://snyk.io/test/github/jackseceng/LinkShort/badge.svg)](https://snyk.io/test/github/jackseceng/LinkShort)
[![CodeQL](https://github.com/jackseceng/LinkShort/actions/workflows/codeql.yml/badge.svg)](https://github.com/jackseceng/LinkShort/actions/workflows/codeql.yml)
[![Grype](https://github.com/jackseceng/LinkShort/actions/workflows/anchore.yml/badge.svg)](https://github.com/jackseceng/LinkShort/actions/workflows/anchore.yml)
[![Docker Build](https://github.com/jackseceng/LinkShort/actions/workflows/docker.yml/badge.svg)](https://github.com/jackseceng/LinkShort/actions/workflows/docker.yml)
![Docker Image Size (tag)](https://img.shields.io/docker/image-size/jackseceng/linkshort/latest)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/jackseceng/LinkShort)

# LinkShort - Containerised URL shortener

This is the Python code and Docker configuration for a link shortening web app

- Running demonstration available at [cubel.ink](https://cubel.ink)

- [DockerHub image repository](https://hub.docker.com/r/jackseceng/linkshort)

I am using this to learn:
- Docker & Web App Hosting
- Python Development
- DevSecOps Automation

## Testing locally

- [Sign up for a free Turso account](https://app.turso.tech/signup), and create database with a table called 'urls' in with the follwing SQL statement:
```
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
docker-compose up -d --build
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
docker-compose down
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
- [x] Demonstration application set up:

> This has been set up on [cloud.run](https://cloud.run) via repository integration

## DevSecOps Automation

- [x] [Super Linter](https://github.com/super-linter/super-linter) Code linting
- [x] [CodeQL](https://codeql.github.com/) Source code vulnerability scanning
- [x] [Snyk](https://snyk.io) Open source dependency vulnerability scanning
- [x] [Grype](https://github.com/anchore/grype/) Container vulnerability scanning
- [x] [Renovate](https://www.mend.io/free-developer-tools/renovate/) Automated dependency upgrades
- [ ] [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) Commit title standardisation
- [x] [Docker Push](https://github.com/docker/build-push-action) Docker image publication on pushes to main branch
- [ ] [Commitizen](https://commitizen-tools.github.io/commitizen/) Automated release management

## Developed by [Jack](https://jacksec.engineer)
