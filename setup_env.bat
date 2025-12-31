@echo off
REM Setup script for FastAPI environment

echo Creating .env file...
(
echo # Project Configuration
echo PROJECT_NAME=Londa APIs
echo VERSION=1.0.0
echo DESCRIPTION=FastAPI backend for Londa Rides CC
echo API_V1_STR=/api/v1
echo.
echo # Server Configuration
echo HOST=0.0.0.0
echo PORT=8000
echo DEBUG=False
echo.
echo # CORS Configuration (comma-separated)
echo BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:8080
echo.
echo # Database Configuration (optional)
echo # DATABASE_URL=postgresql://user:password@localhost:5432/londa_db
echo.
echo # Security
echo SECRET_KEY=your-secret-key-change-in-production
echo ALGORITHM=HS256
echo ACCESS_TOKEN_EXPIRE_MINUTES=30
echo.
echo # Firebase Configuration (optional)
echo # FIREBASE_CREDENTIALS_PATH=./path/to/firebase-credentials.json
echo.
echo # Google Maps API (optional)
echo # GOOGLE_MAPS_API_KEY=your-google-maps-api-key
) > .env

echo .env file created successfully!
echo.
echo Environment setup complete!
echo.
echo To activate the virtual environment, run:
echo   venv\Scripts\activate
echo.
echo To run the application, use:
echo   python run.py
echo   OR
echo   uvicorn app.main:app --reload
pause

