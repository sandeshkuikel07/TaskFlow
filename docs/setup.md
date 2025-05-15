# Local Development Setup

## Prerequisites

* Python 3.11+
* pip

## Steps

1. Clone the repository:

```bash
git clone https://github.com/sandeshkuikel07/TaskFlow.git
cd taskflow
```

2. Create a virtual environment and activate it:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the API server:

```bash
python run.py
```

5. Access:

* Health check: [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)
* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)