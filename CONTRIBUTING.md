# Contributing to the LinkShort project

## Project Objectives

- This is a Python Flask app that shortens URLs and re-directs users that go to the shortened URLs.
- It uses Docker to create an image with a web service.
- It uses [Turso](https://turso.tech) as a database to store URLs.
- The repository uses automated DevSecOps tooling to detect vulnerabilities and bugs.
- If there are any patchable, exploitable vulnerabilities, they will be applied if they build and test successfully.
- Usage and/or contribution to this project must be done under the terms in the `LICENSE` file.

## Testing locally

> Follow the instructions in the `readme` to test locally on your machine, please ensure that you can perform these steps before contributing to this project
- Any issues with testing locally should be raised as a bug on GitHub Issues
- Any fixes or workarounds for identified bugs should be raised on a relevant GitHub Issue

## Making PRs

> Vulnerabilities of medium criticality or higher must be fixed or justified in your PR.

> Before raising a PR, please run the following tools on your work, PR checks run the same tooling.
- [Snyk](https://docs.snyk.io/scan-using-snyk/working-with-snyk-in-your-environment/running-scans#run-tests-manually)
- [Grype](https://github.com/anchore/grype/?tab=readme-ov-file#getting-started)
- [Scout](https://docs.docker.com/scout/quickstart/)
- [Trivy](https://trivy.dev/latest/docs/target/container_image/)

> Your commits must use the [Conventional Commits format](https://www.conventionalcommits.org/en/v1.0.0/)
- It is recommended that you write your commits with [commitizen](https://commitizen-tools.github.io/commitizen/) to ensure consistency


## Support Expectations

> The people listed in the `CODEOWNERS` file will aim to give to support when they can, but they are not obliged to.
- To raise a feature request or bug, please do so in GitHub Issues, using the templates provided. Aim to document as much detail as possible to assist with troubleshooting
- Any offensive or abusive language in tickets will result in a closure of the issue, and a ban from this repository for the offending user
- Any impatience will only waste yours and the code owners time, do not expect any rigid response times for issues raised.
> Any community based support given must be in adherance to the rules written in the `CODE_OF_CONDUCT` file
- Breaches of this behaviour will not be tolerated, and will result in a ban from this repository for the offending user
> Components of the software supply chain for this project will be patched if there is a remediation for an exploitable vulnerablility available.
- If this breaks fucntionality, this is unfortunate, but ultimately intended as per the primary objectives above.
