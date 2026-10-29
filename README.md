# Expense Tracker API

FastAPI + SQLAlchemy + Supabase (PostgreSQL) + JWT Authentication

## Features
- User registration & JWT login
- Transaction CRUD (user-scoped)
- Filtering by type / category / amount range
- Pytest coverage for CRUD

## Local Setup
1. `python3 -m venv venv && source venv/bin/activate`
2. `pip install -r requirements.txt`
3. Create `.env` with the keys listed below
4. `uvicorn app.main:app --reload`
5. Visit http://127.0.0.1:8000/docs

## .env Example

```bash
DATABASE_URL=postgresql+psycopg2://user:pass@host:6543/postgres?sslmode=require
SECRET_KEY=your_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Live API
# expense-tracker-api
