# Security

## Disclosure Policy

- Please first check [the issues page](https://github.com/jackseceng/LinkShort/issues?q=is%3Aissue%20state%3Aopen%20label%3Abug) to see if your bug has already been reported. If it has, please give it a :+1:and add any additional context you think is useful
- If you have found an unreported bug, you must fill out all fields in [the bug report template](https://github.com/jackseceng/LinkShort/security/advisories/new) for this repository. Incomplete or incorrectly formatted reports will be rejected.

## Tooling

This is a list of tooling used by this repository to find vulnerabilities & bugs.
- PR checks are not currently set to fail if a vulnerability is found, please review your PR scans before requesting a review.
- Unfixed vulnerabilities of medium severity or higher must be justified to a PR reviewer before merging


| Capability | Tool    |
| ---------- | ------- |
| Automated dependency updates    | [Renovate](https://www.mend.io/renovate/)                       |
| Code Bugs                       | [CodeQL](https://codeql.github.com/)                            |
| Dependency Vulnerabilities      | [Snyk](https://snyk.io/product/open-source-security-management/)|
| Container Vulnerabiltiies       | [Grype](https://github.com/anchore/grype/) [Scout](https://docs.docker.com/scout/) [Trivy](https://trivy.dev/latest/docs/target/container_image/) |
