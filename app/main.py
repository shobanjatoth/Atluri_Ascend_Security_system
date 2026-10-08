# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.database.connection import Base, engine
# from app.database import models
# from app.core.config import settings

# Base.metadata.create_all(bind=engine)

# app = FastAPI(
#     title=settings.APP_NAME,
#     description="ATURI ASCEND Employee QR Attendance Management System",
#     version="1.0.0"
# )


# origins = [
#     origin.strip()
#     for origin in settings.CORS_ORIGINS.split(",")
#     if origin.strip()
# ]


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.get("/")
# def root():
#     return {
#         "application": settings.APP_NAME,
#         "status": "running",
#         "version": "1.0.0"
#     }


# @app.get("/health")
# def health_check():
#     return {
#         "status": "healthy"
#     }

from app.api.audit_routes import router as audit_router
from app.api.dashboard_routes import router as dashboard_router
from app.api.attendance_routes import router as attendance_router
from app.api.qr_routes import router as qr_router
from app.api.employee_routes import router as employee_router
from app.api.department_routes import router as department_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.report_routes import router as report_router
from app.core.config import settings
from app.database.connection import Base, engine
from app.database import models
from app.api.auth_routes import router as auth_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.APP_NAME,
    description="ATURI ASCEND Employee QR Attendance Management System",
    version="1.0.0"
)


origins = [
    origin.strip()
    for origin in settings.CORS_ORIGINS.split(",")
    if origin.strip()
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(department_router)
app.include_router(employee_router)
app.include_router(qr_router)
app.include_router(attendance_router)
app.include_router(dashboard_router)
app.include_router(report_router)
app.include_router(audit_router)


@app.get("/")
def root():
    return {
        "application": settings.APP_NAME,
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}