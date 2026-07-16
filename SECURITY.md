# Security Policy

## Supported Versions

ReproPilot is currently in active research-software development.

| Version | Supported |
|---|---|
| 0.1.x | Yes |
| Earlier prototypes | No |

## Reporting a Vulnerability

Do not open a public GitHub issue for a vulnerability that could expose users,
systems, credentials, or private repository information.

Report security concerns privately to:

**Suzan Anwar**  
sanwar@philander.edu

Please include:

- a description of the issue;
- affected files or components;
- reproduction steps;
- potential impact;
- suggested mitigation, when available.

## Current Security Scope

ReproPilot is designed to:

- accept local repository paths or public HTTPS GitHub URLs;
- perform shallow temporary clones;
- avoid executing source code from assessed repositories;
- remove temporary clones after assessment;
- run deterministic analysis locally;
- use local Ollama inference when AI is enabled.

Users should still run ReproPilot in an appropriately isolated environment
when assessing untrusted repositories.

## Disclosure

Please allow reasonable time for investigation and remediation before public
disclosure.
