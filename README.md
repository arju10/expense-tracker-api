# 💰 Expense Tracker API

A production-ready RESTful API for personal expense tracking, built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL** (Supabase). It supports secure JWT-based authentication and provides full CRUD operations for income and expense transactions, with strict per-user data isolation.

🚀 **Production URL:** [https://expense-tracker-api-4l7a.onrender.com/](https://expense-tracker-api-4l7a.onrender.com/)

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red)](https://www.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-336791?logo=postgresql&logoColor=white)](https://supabase.com/)


---

## 📑 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the Server](#running-the-server)
- [API Reference](#-api-reference)
  - [Authentication](#authentication)
  - [Transactions](#transactions)
  - [Filtering](#filtering)
- [Testing](#-testing)
- [Author](#-author)

---

## 🧭 Overview

**Expense Tracker API** is a secure, user-scoped backend for managing personal finances. Each user can register, log in, and manage only their own income and expense records. The API follows RESTful conventions and enforces strict ownership checks so that no user can access or modify another user's data.

This project covering the following core topics:

- FastAPI routing and dependency injection
- SQLAlchemy ORM with PostgreSQL
- JWT authentication & authorization
- Pydantic v2 data validation
- Query parameter filtering
- Pytest-based unit testing
- Cloud deployment on Render

---

## ✨ Features

### 🔐 Authentication & Security
- User registration with email and unique username validation
- Password hashing using **bcrypt** (via `passlib`)
- JWT-based authentication with configurable token expiration
- Protected routes via OAuth2 Bearer token scheme
- **Per-user data isolation** — users can never access another user's records

### 💵 Transaction Management
- Create, read, update, and delete transactions
- Automatic ownership assignment (`owner_id`) based on the authenticated user
- Full validation of amount (`> 0`) and type (`income` / `expense`)
- Partial updates supported via `PUT`

### 🔎 Flexible Filtering
- Filter transactions by **type**, **category**, and **amount range**
- All filters are optional and composable

### 🧪 Testing
- 5 core test cases covering the complete CRUD lifecycle
- Integration tests using FastAPI's `TestClient`
- Isolated test users via UUID-based usernames

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) |
| **ORM** | [SQLAlchemy 2.x](https://www.sqlalchemy.org/) |
| **Database** | [PostgreSQL](https://www.postgresql.org/) on [Supabase](https://supabase.com/) |
| **Validation** | [Pydantic v2](https://docs.pydantic.dev/) |
| **Authentication** | [JWT](https://jwt.io/) (`python-jose`) + [passlib](https://passlib.readthedocs.io/) |
| **Testing** | [Pytest](https://docs.pytest.org/) + [HTTPX](https://www.python-httpx.org/) |
| **Server** | [Uvicorn](https://www.uvicorn.org/) |
| **Deployment** | [Render](https://render.com/) |

---

## 📂 Project Structure

```
expense-tracker-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py               # Application entry point
│   ├── config.py             # Environment configuration via pydantic-settings
│   ├── database.py           # SQLAlchemy engine and session factory
│   ├── models.py             # ORM models (User, Transaction)
│   ├── schemas.py            # Pydantic request/response schemas
│   ├── auth.py               # JWT creation, password hashing, current-user dependency
│   └── routers/
│       ├── __init__.py
│       ├── users.py          # /auth routes (register, login)
│       └── transactions.py   # /transactions routes (CRUD + filter)
│
├── tests/
│   └── test_transactions.py  # 5 integration tests
│
├── .env.example              # Example environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Python** 3.12 or higher
- **PostgreSQL** database (free tier on [Supabase](https://supabase.com/) works great)
- **Git**

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/arju10/expense-tracker-api.git
cd expense-tracker-api

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@HOST:6543/postgres?sslmode=require
SECRET_KEY=your_long_random_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> **Note:** For Supabase, use the **connection pooler** URL (port `6543`) and append `?sslmode=require`.
> If your password contains special characters (`@`, `:`, `#`, `/`), URL-encode it first.

You can generate a strong `SECRET_KEY` with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Running the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- **Application:** http://127.0.0.1:8000
- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

Database tables are automatically created on first startup.

---

## 📡 API Reference

Base URL (local): `http://127.0.0.1:8000`
Base URL (live): `https://YOUR-APP.onrender.com`

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:-------------:|
| `POST` | `/auth/register` | Register a new user | ❌ |
| `POST` | `/auth/login` | Obtain a JWT access token | ❌ |

#### `POST /auth/register`

**Request body:**

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secret123"
}
```

**Response `201 Created`:**

```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com"
}
```

#### `POST /auth/login`

> Login accepts **form data** (`application/x-www-form-urlencoded`), not JSON — this is the standard OAuth2 password flow.

**Form fields:** `username`, `password`

**Response `200 OK`:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

Use the token as a Bearer credential on all protected endpoints:

```
Authorization: Bearer <access_token>
```

---

### Transactions

All endpoints below require a valid JWT.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/transactions/` | Create a transaction |
| `GET` | `/transactions/` | List all transactions of the current user |
| `GET` | `/transactions/{id}` | Get one transaction by ID |
| `PUT` | `/transactions/{id}` | Update a transaction |
| `DELETE` | `/transactions/{id}` | Delete a transaction |

#### `POST /transactions/`

**Request body:**

```json
{
  "title": "Monthly Salary",
  "amount": 5000,
  "type": "income",
  "category": "Work",
  "date": "2026-10-29"
}
```

**Response `201 Created`:**

```json
{
  "id": 1,
  "title": "Monthly Salary",
  "amount": 5000.0,
  "type": "income",
  "category": "Work",
  "date": "2026-10-29",
  "owner_id": 1
}
```

**Validation rules:**
- `amount` must be **> 0**
- `type` must be `"income"` or `"expense"`

#### `PUT /transactions/{id}`

Accepts **partial** updates — include only the fields you want to change:

```json
{
  "amount": 6000
}
```

#### `DELETE /transactions/{id}`

**Response `200 OK`:**

```json
{
  "message": "Transaction deleted successfully"
}
```

---

### Filtering

#### `GET /transactions/filter`

Returns filtered transactions belonging to the logged-in user.

**Query parameters:**

| Parameter | Type | Example | Description |
|-----------|------|---------|-------------|
| `type` | string | `expense` | Filter by `income` or `expense` |
| `category` | string | `Food` | Filter by category name |
| `minimum_amount` | float | `100` | Lower bound (inclusive) |
| `maximum_amount` | float | `5000` | Upper bound (inclusive) |

**Example:**

```
GET /transactions/filter?type=expense&category=Food&minimum_amount=100&maximum_amount=5000
```

---

## 🧪 Testing

Run the complete test suite:

```bash
python -m pytest -v
```

**Expected output:**

```
tests/test_transactions.py::test_create_transaction PASSED          [ 20%]
tests/test_transactions.py::test_get_transactions PASSED            [ 40%]
tests/test_transactions.py::test_get_specific_transaction PASSED    [ 60%]
tests/test_transactions.py::test_update_transaction PASSED          [ 80%]
tests/test_transactions.py::test_delete_transaction PASSED          [100%]

==================== 5 passed ====================
```

**Test coverage:**

| Test | What it verifies |
|------|------------------|
| `test_create_transaction` | A transaction is created with the correct data and `201` status |
| `test_get_transactions` | The list endpoint returns all transactions for the authenticated user |
| `test_get_specific_transaction` | Fetching by ID returns the correct record |
| `test_update_transaction` | Partial `PUT` updates the correct field |
| `test_delete_transaction` | Deletion removes the row and returns a confirmation |

---

## 👤 Author

**Mst. Tahmmina Jerin Arju**

- GitHub: [@arju10](https://github.com/arju10)
- Email: mst.tahminajerinarju@gmail.com

---

