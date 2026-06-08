# 🎓 Capstone Project: Async Course Enrollment API

A high-performance, asynchronous REST API built with FastAPI, PostgreSQL, and SQLAlchemy. This platform handles secure user authentication, role-based course administration, and conflict-free student enrollments.

---

## 🚀 Features

- **Asynchronous Architecture**: Full async/await implementation leveraging `asyncpg` for database operations.
- **Robust Authentication**: Secure JWT token generation and OAuth2 password flows.
- **Role-Based Access Control (RBAC)**: Distinct permissions enforced for `admin` and `student` roles.
- **Automated Validation**: Data payload integrity verified via Pydantic V2 schemas.
- **High-Performance Test Suite**: Isolated integration tests using an in-memory SQLite backend.

---

## 🛠️ Project Structure

```text
CAPSTONE_PROJECT/
├── app/
│   ├── core/          # Database connection, config, and security configurations
│   ├── dependencies/  # Authentication tokens and RBAC middleware guards
│   ├── models/        # SQLAlchemy database models
│   ├── repositories/  # Database access layer query definitions
│   ├── routers/       # API endpoints grouped by feature routers
│   ├── schemas/       # Pydantic data validation contracts
│   └── main.py        # Application initialization entry point
├── tests/
│   ├── conftest.py    # Global testing database fixtures and lifecycle hooks
│   ├── pytest.ini     # Pytest execution parameters configuration
│   ├── test_auth.py   # Registration and verification authentication suite
│   ├── test_courses.py# Admin course administration lifecycle testing
│   ├── test_enrollments.py # Enrollment capacity logic validation suite
│   └── test_users.py  # Profile endpoint session parsing test
└── README.md
```

---

## 💻 Local Environment Setup

### 1. Prerequisites
- Python 3.10+
- PostgreSQL database engine instance running locally

### 2. Installation Steps

Clone the repository and enter your project root folder:
```bash
cd CAPSTONE_PROJECT
```

Create and activate a virtual environment:
```bash
python -m venv .venv
# On Windows PowerShell:
.venv\Scripts\Activate.ps1
# On Mac/Linux terminal:
source .venv/bin/activate
```

Install all core application and testing dependencies:
```bash
pip install -r requirements.txt
```

### 3. Database Initialization
Create your production/development PostgreSQL database, then create a completely distinct database for running automated tests:
1. `my_db` (Development)
2. `my_db_test` (Automated testing target)

---

## 🏃 Running the Application

To launch your development server locally, execute:
```bash
uvicorn app.main:app --reload
```
Once active, you can access your interactive swagger documentation interface at: **`http://127.0.0`**

---

## 🧪 Running the Automated Test Suite

The test suite completely avoids database conflicts on Windows by running migrations over a virtual, in-memory SQLite pipeline (`sqlite+aiosqlite`).

### Run all tests together:
```bash
pytest
```

### Run a single specific test file:
```bash
pytest tests/test_courses.py -v
```
