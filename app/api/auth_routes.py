from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import User
from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.core.rate_limit import login_rate_limiter
from app.schemas.auth import LoginRequest, TokenResponse

from app.services.auth_service import (
    authenticate_user,
    generate_login_token,
)

from app.services.audit_service import create_audit_log

from app.core.dependencies import (
    get_current_user,
    require_admin,
)


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)




def login(
    request: Request,
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    client_ip = "unknown"

    if request.client is not None:
        client_ip = request.client.host

    if not login_rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Please try again later.",
        )

    device_info = request.headers.get("user-agent")

    user = authenticate_user(
        db=db,
        username=login_data.username,
        password=login_data.password,
    )

    # Failed login
    if user is None:
        create_audit_log(
            db=db,
            user_id=None,
            action="LOGIN_FAILED",
            ip_address=client_ip,
            device_info=device_info,
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # Successful login
    access_token = generate_login_token(
        db=db,
        user=user,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        username=user.username,
        role=user.role,
    )


@router.get("/me")
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role,
        "is_active": current_user.is_active,
    }


@router.get("/admin-test")
def admin_test(
    current_user: User = Depends(require_admin),
):
    return {
        "message": "Admin authorization successful",
        "user": current_user.username,
        "role": current_user.role,
    }