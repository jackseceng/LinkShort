[![Known Vulnerabilities](https://snyk.io/test/github/jackseceng/LinkShort/badge.svg)](https://snyk.io/test/github/jackseceng/LinkShort)
[![CodeQL](https://github.com/jackseceng/LinkShort/actions/workflows/codeql.yml/badge.svg)](https://github.com/jackseceng/LinkShort/actions/workflows/codeql.yml)
[![Grype](https://github.com/jackseceng/LinkShort/actions/workflows/anchore.yml/badge.svg)](https://github.com/jackseceng/LinkShort/actions/workflows/anchore.yml)
[![Docker Build](https://github.com/jackseceng/LinkShort/actions/workflows/docker.yml/badge.svg)](https://github.com/jackseceng/LinkShort/actions/workflows/docker.yml)
![Docker Image Size (tag)](https://img.shields.io/docker/image-size/jackseceng/linkshort/latest)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/jackseceng/LinkShort)

# LinkShort - Containerised URL shortener

This is the Python code and Docker configuration for a link shortening web app

**This is not a functional application yet,  I will make a full release when it is in a secure, production ready state**

I am using this to learn:
- Docker & Web App Hosting
- Python Development
- DevSecOps Automation

## Testing locally

- [Sign up for a free Turso account](https://app.turso.tech/signup), and create database with a table called 'links' in it.

- Create a file in the `/src` directory called `.env`, with the following contents, setting the appropriate values with your own substitutions:
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

- [x] Simple URL shortening capabilities for URLs
- [x] Sanitises input from user for both URLs and extensions on requests
- [x] Checks user input for URLs that begin with *HTTPS* only
- [ ] Checks submitted URLs for internet reputation before generating them, reject poor reputation URLs
- [x] Generates QR codes for users to download and share
- [x] Frontend with good looking CSS and HTML animations and colours
- [x] Handles errors gracefully, with 404 and 500 error pages rendered to the users
- [x] Containerised with docker compose using secrets management for credentials
- [ ] Demonstration application set up and deployed on hosting provider

## DevSecOps Automation

- [x] [Super Linter](https://github.com/super-linter/super-linter) Code linting for all languages
- [x] [CodeQL](https://codeql.github.com/) Security bug scanning for source code
- [x] [Snyk](https://snyk.io) Vulnerability scanning for open source dependencies
- [x] [Grype](https://github.com/anchore/grype/) Container vulnerability scanning
- [x] [Renovate](https://www.mend.io/free-developer-tools/renovate/) Automated dependency upgrades
- [x] [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) Commit title standardisation
- [x] [Docker Push](https://github.com/docker/build-push-action) Docker image publication on pushes to main branch
- [ ] [Commitizen](https://commitizen-tools.github.io/commitizen/) Automated release management

## Developed by Jack
![Alt Text](https://raw.githubusercontent.com/jacksec/jacksec.github.io/master/assets/img/logo.png)

[My site](https://jacksec.engineer)

