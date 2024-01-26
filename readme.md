# LinkShort - Containerised URL shortener

This is the Python code and Docker/Kubernetes configuration for a link shortening web app

**This is not a functional application yet:**

> I will make a full release on this repo when it is in a secure, working state

I am using this to learn:
- Docker & Kubernetes
- Python web app development 
- DevSecOps automation

## Testing locally:

### Docker compose
- From root directory of repo:
```
$ docker-compose up --detach --scale redis-master=1 --scale redis-replica=3
```
```
[+] Running (6/6)
 ✔ Container linkshort-app-1
 ✔ Container linkshort-redis-replica-2
 ✔ Container linkshort-redis-replica-3
 ✔ Container linkshort-redis-replica-1
 ✔ Container linkshort-redis-master-1
 ✔ Network linkshort_ls-net
```

- If succesful, app will be running at [http://localhost:5000](http://localhost:5000), with a redis master database with 3 replica nodes.

## Application Features:

- [x] Simple URL shortening capabilities for URLs
- [x] Sanitises input from user for both URLs and extensions on requests
- [x] Checks user input for URLs that begin with *https* only
- [ ] Checks submitted URLs for internet reputation before generating them, reject poor reputation URLs
- [x] Nice looking front end CSS and HTML
- [x] Handles errors gracefully, with 404 and 500 error pages rendered to the users
- [x] Containerised with docker compose using 
- [ ] Kubernetes deployment configuration with database in stateful sets
- [ ] Demonstration application set up and deployed on cloud provider

#### (Current features have a checkmark, planned ones do not)

## DevSecOps Automation:

- [x] [Pylint](https://pylint.org/) Python linting
- [x] [Semgrep](https://semgrep.dev/) Code security linting
- [x] [Hadolint](https://github.com/hadolint/hadolint) Dockerfile linting
- [ ] [Renovate](https://www.mend.io/free-developer-tools/renovate/) Automated dependency upgrades
- [ ] [Commitizen](https://commitizen-tools.github.io/commitizen/) Commit standardisation

#### (Current automations have a checkmark, planned ones do not)

## Developed by Jack:
![Alt Text](https://raw.githubusercontent.com/jacksec/jacksec.github.io/master/assets/img/logo.png)

https://jacksec.engineer
