# Docker Deployment

## Build and Run with Docker Compose

```bash
docker-compose up --build
```

This will start:

* `taskflow` - FastAPI backend on port 8000
* `db` - PostgreSQL database on port 5432

## Accessing the Application

* API: [http://localhost:8000](http://localhost:8000)
* Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

To stop:

```bash
docker-compose down
```

## docs/api.md

# API Reference

## Tasks

* `GET /api/tasks/` - List all tasks
* `POST /api/tasks/` - Create a task
* `GET /api/tasks/{id}` - Get a specific task
* `PUT /api/tasks/{id}` - Update a task
* `DELETE /api/tasks/{id}` - Delete a task

## Categories

* `GET /api/categories/` - List all categories
* `POST /api/categories/` - Create a category
* `GET /api/categories/{id}` - Get a specific category
* `PUT /api/categories/{id}` - Update a category
* `DELETE /api/categories/{id}` - Delete a category
