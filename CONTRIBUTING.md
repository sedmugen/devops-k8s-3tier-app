# Contributing Guidelines

Thank you for your interest in contributing to **devops-k8s-3tier-app**! This document provides guidelines for code standards, git workflows, and pull request submissions.

---

## 1. Git Workflow & Branch Naming

All work should be performed in dedicated branches off `main`.

### Branch Format
```
<category>/<short-description>
```

**Approved categories:**
- `feature/` — New features or functional enhancements
- `bugfix/` — Bug fixes
- `docs/` — Documentation updates
- `chore/` — Tooling, dependency, or config maintenance
- `refactor/` — Code refactoring without behavioral changes
- `test/` — Adding or improving tests

*Example:* `feature/connection-pooling`, `docs/architecture-diagram`

---

## 2. Commit Guidelines — Conventional Commits

We strictly follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(optional-scope): description
```

**Approved types:**
- `feat` — New feature
- `fix` — Bug fix
- `refactor` — Code restructuring
- `docs` — Documentation changes
- `style` — Formatting, linting, missing semicolons
- `test` — Adding or modifying tests
- `chore` — Build tasks, package manager configs
- `ci` — CI/CD pipeline modifications

### Commit Rules:
- Write in the **imperative mood** ("add feature", not "added feature").
- Limit the first line to **72 characters**.
- One logical change per commit.
- **Never use vague messages** such as `Update`, `Fix`, `Changes`, or `asdf`.

---

## 3. Code Standards & Linting

- **Python:** Follow PEP 8 guidelines. Verify using `flake8` or `black`.
- **Docker:** Follow container security best practices (non-root users, explicit base image tags).
- **Kubernetes:** Ensure all manifests include labels, health probes, resource requests, and resource limits.

---

## 4. Submitting a Pull Request

1. Fork the repository and create your feature branch.
2. Ensure all tests pass: `pytest` in `app/flask-api/`.
3. Submit a Pull Request targeting `main`.
4. Provide a clear description of changes and verification steps in the PR template.
