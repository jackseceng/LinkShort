# LinkShort - Containerised URL shortener

This is the Python code and Docker/Kubernetes configuration for a link shortening web app

**This is not a functional application yet:**

> I will make a full release on this repo when it is in a secure, working state

I am using this to learn:
- Docker & Kubernetes
- Python web app development 
- DevSecOps automation

## Testing locally:

### Build docker image locally
From root directory of repo:
```
docker-compose build linkshort
```
> [+] Building (10/10) FINISHED
```
docker-compose up linkshort
```

> [+] Running 2/2
>
> Network linkshort_default Created
>
> Container linkshort       Created
>
> Attaching to linkshort
>
>linkshort  |  [1] [INFO] Starting gunicorn 20.1.0
>
>linkshort  |  [1] [INFO] Listening at: http://0.0.0.0:80 (1)
>
>linkshort  |  [1] [INFO] Using worker: sync
>
>linkshort  |  [7] [INFO] Booting worker with pid: 7

### Create a kubernetes cluster with [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/)
From root directory of repo:
```
kubectl deploy -f ./kubernetes/deployments/deployment.yaml
```
> deployment.apps/linkshort-deploy configured
```
kubectl deploy -f ./kubernetes/services/service.yaml
```
> service/linkshort-service created

```
kubectl get deploy
```

| NAME             | READY | UP-TO-DATE | AVAILABLE | AGE   |
|------------------|-------|------------|-----------|-------|
| linkshort-deploy | 2/2   | 2          | 2         | *age* |

```
kubectl get pods  
```

| NAME             | READY | STATUS     | RESTARTS  | AGE   |
|------------------|-------|------------|-----------|-------|
| linkshort-deploy | 1/1   | Running    | 0         | *age* |
| linkshort-deploy | 1/1   | Running    | 0         | *age* |

```
kubectl get svc   
```

|NAME               | TYPE         | CLUSTER-IP   | EXTERNAL-IP | PORT(S)      | AGE   |
|-------------------|--------------|--------------|-------------|--------------|-------|
| kubernetes        | ClusterIP    | *cluster_ip* | none        | 443/TCP      | *age* |
| linkshort-service | LoadBalancer | *lb_ip*      | localhost   | 80:30623/TCP | *age* |


If succesful, app will be running at [http://127.0.0.1](http://127.0.0.1) on port `80`

## Application Features:

- [x] Simple URL shortening capabilities for URLs
- [x] Checks user input for URLs that begin with *https* only
- [ ] Checks submitted URLs for internet reputation before generating them, reject poor reputation URLs
- [x] Nice looking front end CSS and HTML
- [x] Handles errors gracefully, with 404 and 500 error pages rendered to the users
- [x] Containerised with docker
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
