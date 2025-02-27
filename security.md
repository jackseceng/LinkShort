# Security

## Disclosure Policy

If you find a bug please first check [the issues page for open bugs](https://github.com/jackseceng/LinkShort/issues?q=is%3Aissue%20state%3Aopen%20label%3Abug)

- If your bug is already a reported issue, please give it a like and add any additional context you think is useful

- If your bug is not on the status page, please [report a vulnerability on the repository security page](https://github.com/jackseceng/LinkShort/security/advisories/new)

## Security-related tooling

This is a list of tooling used by this repository to find vulnerabilities & bugs.

| Capability | Tool    |
| ---------- | ------- |
| Automated dependency updates    | [Renovate](https://www.mend.io/renovate/)                       |
| Code Bugs                       | [CodeQL](https://codeql.github.com/)                            |
| Dependency Vulnerabilities      | [Snyk](https://snyk.io/product/open-source-security-management/)|
| Container Vulnerabiltiies       | [Grype](https://github.com/anchore/grype/)                      |

## Future security enhancements

- Database entries are not encypted at rest, will implement with hashsums from extensions generated. Docummented in [issue 177](https://github.com/jackseceng/LinkShort/issues/177)
