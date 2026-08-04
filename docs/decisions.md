# Architectural Decision Records (ADR)

This document records the key architectural and design decisions made during the development and refactoring of **devops-k8s-3tier-app**.

---

## ADR-001: Nginx as Presentation Tier Reverse Proxy

### Status
Accepted

### Context
Client requests to backend API services require centralized routing, SSL termination capability, CORS header management, and security header enforcement. Direct exposure of backend application containers increases attack surfaces.

### Decision
We use Nginx Alpine as an independent presentation tier proxy container. All client connections hit Nginx on port 80/30080, which proxies traffic internally to `http://flask-api:5000`.

### Consequences
- **Positive:** Centralized security headers (`X-Frame-Options`, `X-Content-Type-Options`), isolated backend network, clean URL routing.
- **Negative:** Adds one extra network hop between client and backend API.

---

## ADR-002: Production WSGI Server Selection (Gunicorn)

### Status
Accepted

### Context
Flask's built-in WSGI server (`app.run()`) is single-threaded, unoptimized for concurrent connections, and explicitly warned against for production use.

### Decision
We run Flask using **Gunicorn** (`gunicorn -w 4 -b 0.0.0.0:5000 app:app`) inside the container image.

### Consequences
- **Positive:** Multi-worker concurrency, request worker recycling, stability under load.
- **Negative:** Requires minor container build configuration adjustments and dependency inclusion (`gunicorn` in `requirements.txt`).

---

## ADR-003: MySQL Connection Pooling

### Status
Accepted

### Context
Creating a new TCP database connection on every incoming HTTP request generates significant overhead and causes connection starvation under burst traffic.

### Decision
We implement a thread-safe connection pool using `mysql.connector.pooling.MySQLConnectionPool` in Flask. Connections are checked out per request and returned to the pool immediately upon request completion.

### Consequences
- **Positive:** Dramatically reduced database handshake latency, efficient resource utilization.
- **Negative:** Requires handling connection staleness and fallback retry logic during initial container boot.

---

## ADR-004: Kubernetes Expose Strategy (NodePort for Minikube)

### Status
Accepted

### Context
The application needs to run on local single-node Kubernetes environments (Minikube) without requiring cloud load balancer controllers or ingress dependencies.

### Decision
Nginx is exposed via a `NodePort` Service on port `30080`. Internal services (`flask-api` and `mysql`) remain strictly restricted to `ClusterIP` Services.

### Consequences
- **Positive:** Works out of the box on any Minikube setup without extra add-ons.
- **Negative:** Fixed NodePort numbers (30080) can potentially conflict with other local services if port availability is not managed.
