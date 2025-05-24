# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.routes import api_router as api_v1_router # <--- IMPORT THIS
from app.websockets.routes import websocket_router 

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url=f"/api/v1/openapi.json" # Standardize OpenAPI doc path
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.PARSED_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_v1_router, prefix="/api/v1") # <--- ADD THIS LINE
app.include_router(websocket_router)

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} v{settings.PROJECT_VERSION}"}

# Placeholder for startup events (e.g., DB connection check)
@app.on_event("startup")
async def startup_event():
    print("Application startup...")
    # You can add DB connection checks or initializations here
    pass

@app.on_event("shutdown")
async def shutdown_event():
    print("Application shutdown...")
    pass