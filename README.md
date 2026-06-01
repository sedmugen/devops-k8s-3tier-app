# Assignment 3 - DevOps and Kubernetes Pipeline

This project implements a complete 3-tier application using Nginx, Flask API, and MySQL.

The application is containerized using Docker Compose, pushed through GitHub Actions CI/CD, and deployed on Kubernetes using Minikube.

## Project Components

- Nginx is used as a reverse proxy.
- Flask API handles the backend endpoints.
- MySQL stores application data.
- Docker Compose runs the local containerized stack.
- Kubernetes manifests deploy the same application on Minikube.

## Kubernetes Deployment

The Kubernetes setup uses a separate namespace named assignment3.

MySQL uses a PersistentVolume and PersistentVolumeClaim for data persistence. Flask and MySQL use ClusterIP services for internal communication, while Nginx uses a NodePort service to expose the application.
