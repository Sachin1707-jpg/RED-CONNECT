from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import route files
from routes import donor
from routes import hospital
from routes import ngo
from routes import requests
from routes import admin
from routes import matching 

app = FastAPI(
    title="RedConnect API",
    description="Backend API for RedConnect Blood Donation Platform",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React local
        "http://localhost:5173",  # Vite local
        "*"                       # Remove in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routes
app.include_router(
    donor.router,
    prefix="/api",
    tags=["Donors"]
)

app.include_router(
    hospital.router,
    prefix="/api",
    tags=["Hospitals"]
)

app.include_router(
    ngo.router,
    prefix="/api",
    tags=["NGOs"]
)

app.include_router(
    requests.router,
    prefix="/api",
    tags=["Blood Requests"]
)

app.include_router(
    admin.router,
    prefix="/api",
    tags=["Admin"]
)
app.include_router(
    matching.router,
    prefix="/api",
    tags=["Matching"]
)
# Root Endpoint
@app.get("/")
def home():
    return {
        "status": "success",
        "message": "RedConnect Backend Running 🚀"
    }

# Health Check
@app.get("/health")
def health_check():
    return {
        "server": "online",
        "database": "csv",
        "status": "healthy"
    }