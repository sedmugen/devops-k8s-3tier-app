# Changelog

All notable changes to **devops-k8s-3tier-app** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-08-04

### Added
- Created `LICENSE` (MIT License) credited to `sedmugen`.
- Created `.env.example` template for database credentials and application settings.
- Created `CONTRIBUTING.md` and `CHANGELOG.md` repository documentation.
- Created `docs/architecture.md`, `docs/api.md`, and `docs/decisions.md` detailing design architecture, API endpoints, and ADRs.
- Created `assets/images/architecture.svg` visual architecture diagram.
- Created `tests/` directory with `conftest.py` and `test_api.py` implementing automated unit and integration tests using Pytest.
- Added Gunicorn production WSGI server to `app/flask-api/requirements.txt` and Dockerfile.
- Added MySQL connection pooling in Flask backend.
- Added security response headers in Nginx configuration.
- Added non-root `appuser` execution context to Docker images and Kubernetes manifests.

### Changed
- Renamed repository slug to `devops-k8s-3tier-app` for portfolio standards compliance.
- Upgraded `start.sh` script to use dynamic path resolution instead of hardcoded home directory path.
- Refactored `.github/workflows/ci-cd.yml` to include automated testing and linting jobs prior to Docker image build.
- Overhauled `README.md` to follow portfolio standards with badges, architecture visual, installation steps, and API guide.

### Fixed
- Fixed unhandled exceptions and missing input validation on Flask API endpoints.
- Fixed hardcoded DockerHub username references in Kubernetes deployment manifests.
