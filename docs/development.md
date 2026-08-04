# Development & Contribution Guide

This document outlines local development setup, code quality standards, testing workflows, and submission processes for **devops-k8s-3tier-app**.

---

## 1. Local Python Environment Setup

1. Create a Python 3.11 virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -r app/flask-api/requirements.txt
   ```

---

## 2. Running Automated Tests

We use **Pytest** for unit and API integration testing.

### Execute Test Suite
```bash
pytest tests/ -v
```

### Test Suite Structure
- [`tests/conftest.py`](file:///d:/GitHub/assignment3-devops/tests/conftest.py): Pytest fixtures providing Flask test client and database mocks.
- [`tests/test_api.py`](file:///d:/GitHub/assignment3-devops/tests/test_api.py): Unit tests for `/health`, `GET /api/items`, `POST /api/items`, and `DELETE /api/items/<id>`.

---

## 3. Container Build & Testing

Before submitting pull requests, test building containers locally:

```bash
# Build Flask API image
docker build -t sedmugen/flask-api:latest ./app/flask-api

# Build Nginx image
docker build -t sedmugen/nginx-proxy:latest ./app/nginx
```

---

## 4. Coding & Security Standards

- **Python Style:** Adhere to PEP 8 standard formatting.
- **Security:** Do not commit plain text secrets. Use environment variables and secrets templates.
- **Docker Best Practices:** Always specify explicit base image tags and use non-root container users (`USER 10001`).
- **Kubernetes Best Practices:** Ensure all new manifests include resource limits (`requests` & `limits`), liveness/readiness probes, and proper labels.
