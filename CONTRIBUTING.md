# Contributing to the LinkShort project

## Project Objectives

- This is a Python Flask app that shortens URLs and re-directs users that go to the shortened URLs.
- It uses Docker to host the web services that serve web clients.
- It uses [Turso](https://turso.tech) for it's database.
- The repository itself is intended to test the capabiltiies of DevSecOps automation tooling.
- If there are any exploitable vulnerabilities that have a patch available, they will be applied.
- Usage and/or contribution to this project must be done under the terms in the `LICENSE` file.

## Testing locally

> Follow the instructions in the `readme` to test locally on your machine, please ensure that you can perform these steps before contributing to this project
- Any issues with testing locally should be raised as a bug on GitHub Issues
- Any fixes or workarounds for identified bugs should be raised on a relevant GitHub Issue

## Making PRs

> Before raising a PR, please run the following tools on your code to verify that it will pass PR checks:
- [Super Linter Checks](https://github.com/jackseceng/LinkShort/blob/f8a4cc63c7f99f289fa41b05b82673909738ea99/.github/workflows/lint.yml#L36C1-L47C45)
- [Snyk CLI](https://docs.snyk.io/scan-using-snyk/working-with-snyk-in-your-environment/running-scans#run-tests-manually)

## Support Expectations

> The people listed in the `CODEOWNERS` file will aim to give to support when they can, but they are not obliged to.
- To raise a feature request or bug, please do so in GitHub Issues, using the templates provided. Aim to document as much detail as possible to assist with troubleshooting
- Any offensive or abusive language in tickets will result in a closure of the issue, and a ban from this repository for the offending user
- Any impatience will only waste yours and the code owners time, do not expect any rigid response times for issues raised.
> Any community based support given must be in adherance to the rules written in the `CODE_OF_CONDUCT` file
- Breaches of this behaviour will not be tolerated, and will result in a ban from this repository for the offending user
> Components of the software supply chain for this project will be patched if there is a remediation for an exploitable vulnerablility available.
- If this breaks fucntionality, this is unfortunate, but ultimately intended as per the primary objectives above.
