# LinkShort

[![SAST](https://github.com/jackseceng/LinkShort/actions/workflows/codeql.yml/badge.svg)](https://codeql.github.com/)
[![Image Scans](https://github.com/jackseceng/LinkShort/actions/workflows/container.yml/badge.svg)](https://github.com/jackseceng/LinkShort/actions/workflows/container.yml)
![Image Size](https://img.shields.io/docker/image-size/jackseceng/linkshort/latest)
![Codebase Size](https://img.shields.io/github/languages/code-size/jackseceng/LinkShort)

This is the Python code, web assets and Docker configuration for a link shortening web app

- Try out the app at [cubel.ink](https://cubel.ink)

- Download the [DockerHub image](https://hub.docker.com/r/jackseceng/linkshort)

## Testing locally

Below are instructions for setting up the container locally on your machine for testing and development.

### Database

[Sign up for a free Turso account](https://app.turso.tech/signup), and create database with a table called `urls` in with the follwing SQL statement:
```SQL
CREATE TABLE
  urls (
    HASHSUM NUMERIC PRIMARY KEY NOT NULL,
    URL BLOB NOT NULL,
    SALT BLOB NOT NULL,
    CLICKS INTEGER NOT NULL DEFAULT 0,
    LASTCLICK TEXT NOT NULL DEFAULT 'YYYY-MM-DDTHH:MM:SS.ffffff'
  );
```
> [!TIP]
> To avoid cluttering up your database while testing locally, it is recommended you create 2 databases: One for testing and one for production

### Captcha & Web Assets Storage

First, [sign up for a free Cloudflare acccount](https://dash.cloudflare.com/sign-up)

Then, setup a turnstile widget for your TLD and localhost domains, guides are available in [the Cloudflare Turnstile docs](https://developers.cloudflare.com/turnstile/)

Next, setup R2 storage, and link your TLD to the service for production, guides are available in [the Cloudflare R2 docs](https://developers.cloudflare.com/r2/)

Once you have the storage set up, upload your static Javascript and image assets to the route of your bucket, making sure their names match what the HTML files reference in their headers.

> [!TIP]
> If you want to change the static web files files, either point your HTML to your locally hosted version, or upload your changed files to an R2 dev bucket manually running this AWS CLI docker container sync command from the root of the repository:
> ```txt
> docker run --rm -ti -v ~/.aws:/root/.aws -v ./app/static:/data amazon/aws-cli s3 sync /data s3://cubelink-web-assets --endpoint-url https://<your-r2-s3-endpoint>.eu.r2.cloudflarestorage.com
> ```
> Or, if you are outside the EU:
> ```txt
> docker run --rm -ti -v ~/.aws:/root/.aws -v ./app/static:/data amazon/aws-cli s3 sync /data s3://cubelink-web-assets --endpoint-url https://<your-r2-s3-endpoint>.r2.cloudflarestorage.com
> ```

### Local Environment

Create a file in the `/app` directory called `.env`, with the following contents, setting the appropriate values with your own substitutions

> [!TIP]
> If you made separate testing and production databases and R2 buckets, make sure to set the TOKEN, ENDPOINT and CDN values to their endpoints in your `.env` file

```txt
ENDPOINT="<your-turso-url>"
TOKEN="<your-turso-token>"
CF_SECRET="<your-cloudflare-secret-key>"
TLD=localhost
CDN="<your-dev-r2-url>"
```

> [!CAUTION]
> The `docker-compose.yaml` and `.env` files must reference the same variable names where applicable, also make sure the variable names are not set elsewhere in your testing environment.

### Launch Instance

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

## Features

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
- [x] Captcha on main page: Uses [Cloudflare Turnstile](https://www.cloudflare.com/en-gb/application-services/products/turnstile/)
- [x] Static content served through CDN: Served via [Cloudflare R2](https://www.cloudflare.com/en-gb/developer-platform/products/r2/)
- [x] Demonstration application set up: Hosted on [cloud.run](https://cloud.run)
- [x] Custom URLs users enter in the main form
- [x] Statistics page for URLs to see how many clicks links have got (go to `tld/url/stats` to see them)

## DevSecOps

Code Linting:
- [x] [Super Linter](https://github.com/super-linter/super-linter)

Static & Software Composition Analysis:
- [x] [CodeQL](https://codeql.github.com/)
- [x] [Snyk](https://snyk.io)
- [x] [semgrep](https://semgrep.dev/products/semgrep-code/)

Container Image Scanning:
- [x] [Grype](https://github.com/anchore/grype/)
- [x] [Docker Scout](https://docs.docker.com/scout/)
- [x] [Trivy](https://trivy.dev/latest/docs/target/container_image/)

Automated Dependency Upgrades:
- [x] [Renovate](https://www.mend.io/free-developer-tools/renovate/)
- [x] [Dependabot](https://github.com/dependabot)

Commit Standardisation:
- [x] [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)

## Developed by [Jack](https://jacksec.engineer)
