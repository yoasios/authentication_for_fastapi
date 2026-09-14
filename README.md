# FastAPI Authentication System

A complete authentication system with JWT tokens, cookie-based sessions, and password hashing using FastAPI and SQLAlchemy.

## Features

- User registration and login
- JWT token authentication
- HTTP-only cookie support
- Password hashing with passlib
- Protected routes with authentication
- SQLite database with SQLAlchemy

## Setup

1. Install dependencies:
```bash
pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose[cryptography] python-dotenv
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Install packages in venv:
```bash
pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose[cryptography] python-dotenv
```

4. Create `.env` file:
```
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
DATABASE_URL=sqlite:///./test.db
JWT_SECRET_KEY=your-jwt-secret-key-here
```

## Usage

Start the server:
```bash
uvicorn main:app --reload
```

## API Endpoints

### Register User
```
POST /login
Content-Type: application/json

{
  "name": "John",
  "email": "john@example.com",
  "password": "password123"
}
```

### Sign In
```
POST /signin/{email}/{password}
```

### Protected Route
```
GET /protected
```

## File Structure

- `main.py` - Main FastAPI application with endpoints
- `auth.py` - Authentication utilities (JWT, password hashing)
- `database.py` - Database configuration
- `modals.py` - SQLAlchemy models
- `schemas.py` - Pydantic schemas
- `.env` - Environment variables