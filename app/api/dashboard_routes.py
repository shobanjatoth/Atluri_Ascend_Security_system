from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin
from app.database.connection import get_db
from app.database.models import User
from app.schemas.dashboard import (
    DashboardResponse,
    DashboardSummaryResponse,
    DepartmentSummary,
    RecentAttendance,
)
from app.services.dashboard_service import (
    get_dashboard_summary,
    get_department_summary,
    get_recent_attendance,
    get_full_dashboard,
)

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse,
)
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return get_dashboard_summary(db)


@router.get(
    "/departments",
    response_model=list[DepartmentSummary],
)
def dashboard_departments(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return get_department_summary(db)


@router.get(
    "/recent-attendance",
    response_model=list[RecentAttendance],
)
def dashboard_recent_attendance(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return get_recent_attendance(db)


@router.get(
    "",
    response_model=DashboardResponse,
)
def full_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return get_full_dashboard(db)