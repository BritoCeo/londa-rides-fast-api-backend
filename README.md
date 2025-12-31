# Londa APIs - FastAPI Backend

FastAPI backend application for Londa Rides CC ride-sharing platform.

## Features

- 🚀 FastAPI with async/await support
- 📝 Automatic API documentation (Swagger/OpenAPI)
- 🔒 Built-in security and CORS support
- ✅ Input validation with Pydantic
- 🎯 Clean architecture with separation of concerns
- 🛡️ Comprehensive error handling
- ⚙️ Environment-based configuration

## Project Structure

```
londa-apis/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py          # API router aggregation
│   │       └── endpoints/      # API endpoint modules
│   │           ├── __init__.py
│   │           ├── health.py
│   │           └── example.py
│   └── core/
│       ├── __init__.py
│       ├── config.py           # Application configuration
│       └── exceptions.py       # Exception handlers
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository** (if applicable) or navigate to the project directory

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Create environment file**:
   ```bash
   cp .env.example .env
   ```

6. **Edit `.env` file** with your configuration values

## Running the Application

### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## API Endpoints

### Health Check
- `GET /health` - Basic health check
- `GET /api/v1/health/` - API health check
- `GET /api/v1/health/detailed` - Detailed health check

### Example Endpoints
- `GET /api/v1/example/` - Get all items
- `GET /api/v1/example/{item_id}` - Get item by ID
- `POST /api/v1/example/` - Create new item
- `PUT /api/v1/example/{item_id}` - Update item
- `DELETE /api/v1/example/{item_id}` - Delete item

## Development

### Code Formatting

```bash
black app/
```

### Linting

```bash
flake8 app/
```

### Type Checking

```bash
mypy app/
```

### Running Tests

```bash
pytest
```

## Configuration

Configuration is managed through environment variables. See `.env.example` for available options.

Key configuration options:
- `PROJECT_NAME`: Application name
- `DEBUG`: Enable/disable debug mode
- `BACKEND_CORS_ORIGINS`: Allowed CORS origins
- `SECRET_KEY`: Secret key for security (change in production!)
- `DATABASE_URL`: Database connection string (if using database)

## Adding New Endpoints

1. Create a new file in `app/api/v1/endpoints/`
2. Define your router and endpoints
3. Import and include the router in `app/api/v1/api.py`

Example:
```python
# app/api/v1/endpoints/users.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_users():
    return {"users": []}
```

Then in `app/api/v1/api.py`:
```python
from app.api.v1.endpoints import users

api_router.include_router(users.router, prefix="/users", tags=["users"])
```

## Error Handling

The application includes comprehensive error handling:
- Custom exception classes in `app/core/exceptions.py`
- Global exception handlers
- Consistent error response format

## Security

- CORS middleware configured
- Input validation with Pydantic
- Environment-based secret management
- Ready for JWT authentication (uncomment in requirements.txt)

## License

[Your License Here]

## Contributing

[Your Contributing Guidelines Here]

