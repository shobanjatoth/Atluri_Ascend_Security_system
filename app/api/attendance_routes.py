

# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session

# from app.services.audit_service import create_audit_log
# from app.database.connection import get_db
# from app.database.models import Employee, User

# from app.core.dependencies import (
#     get_current_user,
#     require_admin,
# )

# from app.schemas.attendance import (
#     CheckInRequest,
#     CheckInResponse,
#     CheckOutRequest,
#     CheckOutResponse,
#     AttendanceHistoryResponse,
#     AdminAttendanceResponse,
# )

# from app.services.attendance_service import (
#     check_in_employee,
#     check_out_employee,
#     get_employee_attendance_history,
#     get_all_attendance,
# )


# router = APIRouter(
#     prefix="/api/attendance",
#     tags=["Attendance"],
# )


# # ============================================================
# # CHECK-IN
# # ============================================================

# @router.post(
#     "/check-in",
#     response_model=CheckInResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# def check_in(
#     attendance_data: CheckInRequest,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     # Find employee linked to the logged-in user
#     employee = (
#         db.query(Employee)
#         .filter(Employee.user_id == current_user.id)
#         .first()
#     )

#     if employee is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Employee profile not found",
#         )

#     # Employee must be active
#     if employee.status != "ACTIVE":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Employee account is inactive",
#         )

#     try:
#         attendance = check_in_employee(
#             db=db,
#             employee=employee,
#             raw_qr_token=attendance_data.qr_token,
#         )

#         # Create audit log after successful check-in
#         create_audit_log(
#             db=db,
#             user_id=current_user.id,
#             action="CHECK_IN",
#         )

#         return CheckInResponse(
#             message="Check-in successful",
#             attendance_id=attendance.id,
#             employee_id=attendance.employee_id,
#             attendance_date=attendance.attendance_date,
#             check_in=attendance.check_in,
#             status=attendance.status,
#             is_late=attendance.is_late,
#         )

#     except ValueError as error:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=str(error),
#         )


# # ============================================================
# # CHECK-OUT
# # ============================================================

# @router.post(
#     "/check-out",
#     response_model=CheckOutResponse,
#     status_code=status.HTTP_200_OK,
# )
# def check_out(
#     attendance_data: CheckOutRequest,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     # Find employee linked to the logged-in user
#     employee = (
#         db.query(Employee)
#         .filter(Employee.user_id == current_user.id)
#         .first()
#     )

#     if employee is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Employee profile not found",
#         )

#     # Employee must be active
#     if employee.status != "ACTIVE":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Employee account is inactive",
#         )

#     try:
#         attendance = check_out_employee(
#             db=db,
#             employee=employee,
#             raw_qr_token=attendance_data.qr_token,
#         )

#         # Create audit log after successful check-out
#         create_audit_log(
#             db=db,
#             user_id=current_user.id,
#             action="CHECK_OUT",
#         )

#         return CheckOutResponse(
#             message="Check-out successful",
#             attendance_id=attendance.id,
#             employee_id=attendance.employee_id,
#             attendance_date=attendance.attendance_date,
#             check_in=attendance.check_in,
#             check_out=attendance.check_out,
#             working_minutes=attendance.working_minutes,
#             status=attendance.status,
#         )

#     except ValueError as error:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=str(error),
#         )


# # ============================================================
# # MY ATTENDANCE
# # ============================================================

# @router.get(
#     "/my-attendance",
#     response_model=list[AttendanceHistoryResponse],
# )
# def get_my_attendance(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     # Find employee linked to the logged-in user
#     employee = (
#         db.query(Employee)
#         .filter(Employee.user_id == current_user.id)
#         .first()
#     )

#     if employee is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Employee profile not found",
#         )

#     # Employee must be active
#     if employee.status != "ACTIVE":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Employee account is inactive",
#         )

#     return get_employee_attendance_history(
#         db=db,
#         employee=employee,
#     )


# # ============================================================
# # ADMIN - ALL ATTENDANCE
# # ============================================================

# @router.get(
#     "",
#     response_model=list[AdminAttendanceResponse],
# )
# def get_all_attendance_records(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(require_admin),
# ):
#     return get_all_attendance(db=db)









from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Employee, User

from app.core.dependencies import (
    get_current_user,
    require_admin,
)

from app.schemas.attendance import (
    CheckInRequest,
    CheckInResponse,
    CheckOutRequest,
    CheckOutResponse,
    AttendanceHistoryResponse,
    AdminAttendanceResponse,
)

from app.services.attendance_service import (
    check_in_employee,
    check_out_employee,
    get_employee_attendance_history,
    get_all_attendance,
)


router = APIRouter(
    prefix="/api/attendance",
    tags=["Attendance"],
)


# ============================================================
# CHECK-IN
# ============================================================

@router.post(
    "/check-in",
    response_model=CheckInResponse,
    status_code=status.HTTP_201_CREATED,
)
def check_in(
    attendance_data: CheckInRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Find employee linked to the logged-in user
    employee = (
        db.query(Employee)
        .filter(Employee.user_id == current_user.id)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee profile not found",
        )

    # Employee must be active
    if employee.status != "ACTIVE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Employee account is inactive",
        )

    try:
        attendance = check_in_employee(
            db=db,
            employee=employee,
            raw_qr_token=attendance_data.qr_token,
            user_id=current_user.id,
        )

        return CheckInResponse(
            message="Check-in successful",
            attendance_id=attendance.id,
            employee_id=attendance.employee_id,
            attendance_date=attendance.attendance_date,
            check_in=attendance.check_in,
            status=attendance.status,
            is_late=attendance.is_late,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


# ============================================================
# CHECK-OUT
# ============================================================

@router.post(
    "/check-out",
    response_model=CheckOutResponse,
    status_code=status.HTTP_200_OK,
)
def check_out(
    attendance_data: CheckOutRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Find employee linked to the logged-in user
    employee = (
        db.query(Employee)
        .filter(Employee.user_id == current_user.id)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee profile not found",
        )

    # Employee must be active
    if employee.status != "ACTIVE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Employee account is inactive",
        )

    try:
        attendance = check_out_employee(
            db=db,
            employee=employee,
            raw_qr_token=attendance_data.qr_token,
            user_id=current_user.id,
        )

        return CheckOutResponse(
            message="Check-out successful",
            attendance_id=attendance.id,
            employee_id=attendance.employee_id,
            attendance_date=attendance.attendance_date,
            check_in=attendance.check_in,
            check_out=attendance.check_out,
            working_minutes=attendance.working_minutes,
            status=attendance.status,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


# ============================================================
# MY ATTENDANCE
# ============================================================

@router.get(
    "/my-attendance",
    response_model=list[AttendanceHistoryResponse],
)
def get_my_attendance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Find employee linked to the logged-in user
    employee = (
        db.query(Employee)
        .filter(Employee.user_id == current_user.id)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee profile not found",
        )

    # Employee must be active
    if employee.status != "ACTIVE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Employee account is inactive",
        )

    return get_employee_attendance_history(
        db=db,
        employee=employee,
    )


# ============================================================
# ADMIN - ALL ATTENDANCE
# ============================================================

@router.get(
    "",
    response_model=list[AdminAttendanceResponse],
)
def get_all_attendance_records(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return get_all_attendance(db=db)