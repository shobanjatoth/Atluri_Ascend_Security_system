# from fastapi import APIRouter, Depends, Request, status
# from fastapi import APIRouter, Depends, status
# from sqlalchemy.orm import Session
# from app.core.dependencies import require_admin
# from app.database.connection import get_db
# from app.database.models import User
# from fastapi import APIRouter, Depends, Request, status
# from app.core.rate_limit import qr_rate_limiter
# from app.schemas.qr import (
#     QRGenerateResponse,
#     QRValidateRequest,
#     QRValidateResponse,
# )

# from app.services.qr_service import (
#     generate_qr_session,
#     validate_qr_token,
# )

# from app.services.audit_service import create_audit_log


# router = APIRouter(
#     prefix="/api/qr",
#     tags=["QR Management"]
# )


# # ============================================================
# # GENERATE QR
# # ============================================================

# @router.post(
#     "/generate",
#     response_model=QRGenerateResponse,
#     status_code=status.HTTP_201_CREATED
# )
# def generate_qr(
#     location: str | None = None,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(require_admin)
# ):
#     # Generate QR session and raw token
#     qr_session, raw_token = generate_qr_session(
#         db=db,
#         location=location
#     )

#     # Create audit log
#     create_audit_log(
#         db=db,
#         user_id=current_user.id,
#         action="QR_GENERATED",
#     )

#     # Return QR information
#     return QRGenerateResponse(
#         id=qr_session.id,
#         expires_at=qr_session.expires_at,
#         location=qr_session.location,
#         qr_token=raw_token
#     )


# # ============================================================
# # VALIDATE QR
# # ============================================================

# @router.post(
#     "/validate",
#     response_model=QRValidateResponse
# )

# def validate_qr(
#     request: Request,
#     qr_data: QRValidateRequest,
#     db: Session = Depends(get_db),
# ):
#     client_ip = "unknown"

#     if request.client is not None:
#         client_ip = request.client.host

#     if not qr_rate_limiter.is_allowed(client_ip):
#         raise HTTPException(
#             status_code=status.HTTP_429_TOO_MANY_REQUESTS,
#             detail="Too many QR validation requests. Please try again later.",
#         )







# def validate_qr(
#     qr_data: QRValidateRequest,
#     db: Session = Depends(get_db)
# ):
#     # Validate QR token
#     qr_session = validate_qr_token(
#         db=db,
#         raw_token=qr_data.qr_token
#     )

#     # Invalid / expired QR
#     if qr_session is None:
#         return QRValidateResponse(
#             valid=False,
#             message="Invalid or expired QR code"
#         )

#     # Valid QR
#     return QRValidateResponse(
#         valid=True,
#         message="QR code is valid",
#         qr_session_id=qr_session.id,
#         location=qr_session.location,
#         expires_at=qr_session.expires_at
#     )


from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status,
)

from sqlalchemy.orm import Session

from app.core.dependencies import require_admin
from app.core.rate_limit import qr_rate_limiter

from app.database.connection import get_db
from app.database.models import User

from app.schemas.qr import (
    QRGenerateResponse,
    QRValidateRequest,
    QRValidateResponse,
)

from app.services.qr_service import (
    generate_qr_session,
    validate_qr_token,
)

from app.services.audit_service import create_audit_log


router = APIRouter(
    prefix="/api/qr",
    tags=["QR Management"],
)


# ============================================================
# GENERATE QR
# ============================================================

@router.post(
    "/generate",
    response_model=QRGenerateResponse,
    status_code=status.HTTP_201_CREATED,
)
def generate_qr(
    location: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    # Generate QR session and raw token
    qr_session, raw_token = generate_qr_session(
        db=db,
        location=location,
    )

    # Create audit log
    create_audit_log(
        db=db,
        user_id=current_user.id,
        action="QR_GENERATED",
    )

    # Return QR information
    return QRGenerateResponse(
        id=qr_session.id,
        expires_at=qr_session.expires_at,
        location=qr_session.location,
        qr_token=raw_token,
    )


# ============================================================
# VALIDATE QR
# ============================================================

@router.post(
    "/validate",
    response_model=QRValidateResponse,
)
def validate_qr(
    request: Request,
    qr_data: QRValidateRequest,
    db: Session = Depends(get_db),
):
    # Get client IP address
    client_ip = "unknown"

    if request.client is not None:
        client_ip = request.client.host

    # Rate-limit QR validation
    if not qr_rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many QR validation requests. Please try again later.",
        )

    # Validate QR token
    qr_session = validate_qr_token(
        db=db,
        raw_token=qr_data.qr_token,
    )

    # Invalid / expired QR
    if qr_session is None:
        return QRValidateResponse(
            valid=False,
            message="Invalid or expired QR code",
        )

    # Valid QR
    return QRValidateResponse(
        valid=True,
        message="QR code is valid",
        qr_session_id=qr_session.id,
        location=qr_session.location,
        expires_at=qr_session.expires_at,
    )