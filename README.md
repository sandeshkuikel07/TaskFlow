
````markdown
# TaskFlow API - Task Management with FastAPI

A comprehensive task management API built using **FastAPI**, following clean architecture principles and best development practices.

## Features

- Task creation with title, description, due date, and priority levels
- Task categorization and status tracking
- Task filtering and sorting capabilities
- Clean architecture with separate API, service, and data layers
- Comprehensive test coverage using pytest
- Dockerized for easy deployment

## Tech Stack

- **FastAPI** – Modern, fast (high-performance) web framework for building APIs
- **SQLAlchemy** – SQL toolkit and ORM
- **Pydantic v2** – Data validation and settings management
- **PostgreSQL / SQLite** – Database (SQLite for development, PostgreSQL for production)
- **pytest** – Testing framework
- **Docker** – Containerization for deployment

## Setup Instructions

### Prerequisites

- Python 3.11+
- Docker (optional, for containerized setup)

### Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sandeshkuikel07/TaskFlow.git
   cd TaskFlow
````

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the development server**:

   ```bash
   python run.py
   ```

4. **Access the API**:

   * Health Check: [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)
   * Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   * ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Running Tests

To run the test suite with pytest:

```bash
pytest
```

### Environment Variables (.env)

```env
# Environment
ENVIRONMENT=dev

# Database
DATABASE_URL=sqlite:///./taskflow.db

# Security
SECRET_KEY="_security_key_here_"
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:5173
```

## Docker Usage

To run the FastAPI app with PostgreSQL using Docker:

1. **Build and start the containers**:

   ```bash
   docker-compose up --build
   ```

2. The API will be available at: [http://localhost:8000](http://localhost:8000)

## Project Structure

```
TaskFlow/
├── backend/
│   ├── main.py           # FastAPI application entry point
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── database.py       # Database connection
│   ├── config.py         # Configuration using Pydantic settings
│   ├── routes/           # FastAPI route handlers
│   │   ├── __init__.py
│   │   ├── tasks.py
│   │   ├── categories.py
│   │   └── auth.py
├── tests/                # Test suite
│   └── test_api.py
├── run.py                # Script to run the application
├── Dockerfile            # Multi-stage Dockerfile for backend & frontend
├── docker-compose.yml    # Compose for API and PostgreSQL
├── requirements.txt      # Python dependencies
└── .env                  # Environment variables
```

## API Endpoints

### Tasks

* `GET /api/tasks` – List all tasks (with optional filters)
* `POST /api/tasks` – Create a new task
* `GET /api/tasks/{id}` – Get a task by ID
* `PUT /api/tasks/{id}` – Update a task
* `DELETE /api/tasks/{id}` – Delete a task

### Categories

* `GET /api/categories` – List all categories
* `POST /api/categories` – Create a new category
* `GET /api/categories/{id}` – Get a category by ID
* `PUT /api/categories/{id}` – Update a category
* `DELETE /api/categories/{id}` – Delete a category

