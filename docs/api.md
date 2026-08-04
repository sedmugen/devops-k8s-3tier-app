# REST API Documentation

This document provides a detailed specification for the Flask REST API endpoints exposed by **devops-k8s-3tier-app**.

---

## Base URL
- **Local Docker Compose:** `http://localhost:80`
- **Minikube Cluster:** `http://<minikube-ip>:30080`

---

## Endpoints Summary

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | Service health check | No |
| `GET` | `/api/items` | Fetch all items | No |
| `POST` | `/api/items` | Create a new item | No |
| `DELETE` | `/api/items/<id>` | Delete an item by ID | No |

---

## Endpoint Details

### 1. Health Check
Checks the operational status of the Flask API.

- **URL:** `/health`
- **Method:** `GET`
- **Success Response (200 OK):**
  ```json
  {
    "status": "healthy",
    "service": "flask-api"
  }
  ```
- **Example Request:**
  ```bash
  curl -i http://localhost/health
  ```

---

### 2. Get All Items
Retrieves all items stored in the MySQL database ordered by creation timestamp descending.

- **URL:** `/api/items`
- **Method:** `GET`
- **Success Response (200 OK):**
  ```json
  [
    {
      "id": 1,
      "name": "Sample Item",
      "description": "Demonstration item description",
      "created_at": "2026-08-04 18:00:00"
    }
  ]
  ```
- **Example Request:**
  ```bash
  curl -i http://localhost/api/items
  ```

---

### 3. Create Item
Inserts a new item record into the database.

- **URL:** `/api/items`
- **Method:** `POST`
- **Headers:** `Content-Type: application/json`
- **Request Body:**
  ```json
  {
    "name": "New Item Name",
    "description": "Optional item description text"
  }
  ```
- **Success Response (201 Created):**
  ```json
  {
    "id": 2,
    "name": "New Item Name",
    "description": "Optional item description text"
  }
  ```
- **Error Response (400 Bad Request):**
  ```json
  {
    "error": "Name is required"
  }
  ```
- **Example Request:**
  ```bash
  curl -i -X POST http://localhost/api/items \
    -H "Content-Type: application/json" \
    -d '{"name":"Kubernetes Demo","description":"Created via API"}'
  ```

---

### 4. Delete Item
Deletes an item record by its unique numeric ID.

- **URL:** `/api/items/<item_id>`
- **Method:** `DELETE`
- **Success Response (200 OK):**
  ```json
  {
    "message": "Item deleted"
  }
  ```
- **Error Response (404 Not Found):**
  ```json
  {
    "error": "Item not found"
  }
  ```
- **Example Request:**
  ```bash
  curl -i -X DELETE http://localhost/api/items/1
  ```
