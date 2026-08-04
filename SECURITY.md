# Security Policy

## Supported Versions

The following table lists the supported versions of **devops-k8s-3tier-app**:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

---

## Reporting a Vulnerability

We take security issues seriously. If you discover a vulnerability or security flaw in this project, please follow these guidelines:

1. **Do NOT open a public GitHub issue** to report security vulnerabilities.
2. Email details of the vulnerability directly to the project maintainer (`sedmugen`) via GitHub profile contact options.
3. Include the following details in your report:
   - Type of issue (e.g. secret exposure, buffer overflow, SQL injection, privilege escalation).
   - Step-by-step instructions to reproduce the issue.
   - Potential impact and suggested mitigation steps.

---

## Security Best Practices Implemented

- **Non-Root Containers:** All container images run under a dedicated non-root user (`USER 10001` / `appuser`).
- **Secret Separation:** Credentials are excluded from code and injected dynamically via Kubernetes `Secret` resources and environment variables (`.env`).
- **HTTP Security Headers:** Nginx enforces `X-Frame-Options`, `X-Content-Type-Options`, and `X-XSS-Protection`.
- **Parameterize Statements:** All database queries utilize parameterized SQL execution to prevent SQL injection vulnerabilities.
