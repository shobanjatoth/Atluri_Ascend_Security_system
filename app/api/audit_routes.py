from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin
from app.database.connection import get_db
from app.database.models import User
from app.schemas.audit import AuditLogResponse
from app.services.audit_service import get_audit_logs


router = APIRouter(
    prefix="/api/audit",
    tags=["Audit Logs"],
)


@router.get(
    "",
    response_model=list[AuditLogResponse],
)
def audit_logs(
    limit: int = Query(
        default=100,
        ge=1,
        le=500,
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return get_audit_logs(
        db=db,
        limit=limit,
    )