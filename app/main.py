from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url="/api/v1/openapi.json"
)

# CORS - Configure as needed, allowing frontend origin
# if settings.BACKEND_CORS_ORIGINS:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=[str(origin) for origin in settings.PARSED_CORS_ORIGINS],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} v{settings.PROJECT_VERSION}"}

@app.on_event("startup")
async def startup_event():
    print(f"{settings.PROJECT_NAME} is starting up...")
    # Potential DB connection check or initial data seeding here later

@app.on_event("shutdown")
async def shutdown_event():
    print(f"{settings.PROJECT_NAME} is shutting down...")