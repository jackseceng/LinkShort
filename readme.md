# LinkShort - Containerised URL shortener

This is the Python code and Docker configuration for a link shortening web app

**This is not a functional application yet,  I will make a full release when it is in a secure, production ready state**

I am using this to learn:
- Docker & Kubernetes
- Python web app development
- DevSecOps automation

## Testing locally

- [Sign up for a free Turso account](https://app.turso.tech/signup), and create database with a table called 'links' in it.

- Create a file in the `/src` directory called `.env`, with the following contents, setting the appropriate values with your own substitutions:
```txt
ENDPOINT="<your-turso-url>"
TOKEN="<your-turso-token>"
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
 ✔ Network ls-container_ls-net
 ✔ Container ls-container-app-1
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
- [x] Frontend with good looking CSS and HTML animations and colours
- [x] Handles errors gracefully, with 404 and 500 error pages rendered to the users
- [x] Containerised with docker compose using secrets management for credentials
- [ ] Kubernetes deployment configuration with database in stateful sets
- [ ] Demonstration application set up and deployed on cloud provider

### (Current features have a checkmark, planned ones do not)

## DevSecOps Automation

- [x] [Super Linter](https://github.com/super-linter/super-linter) Code linting for all languages on PRs
- [x] [Snyk](https://snyk.io) Automated security scanning and vulnerability patching
- [x] [Renovate](https://www.mend.io/free-developer-tools/renovate/) Automated dependency upgrades
- [x] [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) Commit title standardisation
- [ ] [Commitizen](https://commitizen-tools.github.io/commitizen/) Automated release management

### (Current automations have a checkmark, planned ones do not)

## Developed by Jack
![Alt Text](https://raw.githubusercontent.com/jacksec/jacksec.github.io/master/assets/img/logo.png)

[My site](https://jacksec.engineer)

