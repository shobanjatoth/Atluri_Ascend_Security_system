









# from datetime import datetime
# from app.core.timezone import INDIA_TIMEZONE
# from datetime import time

# from sqlalchemy.orm import Session

# from app.core.timezone import get_current_india_datetime
# from app.database.models import Attendance, Employee
# from app.services.qr_service import validate_qr_token
# from app.services.audit_service import create_audit_log



# def normalize_india_datetime(value: datetime) -> datetime:
#     """
#     Convert an aware datetime to India time and remove timezone information.

#     Naive datetimes are assumed to already represent India time.
#     """
#     if value.tzinfo is not None:
#         return value.astimezone(INDIA_TIMEZONE).replace(tzinfo=None)

#     return value







# def check_in_employee(
#     db: Session,
#     employee: Employee,
#     raw_qr_token: str,
#     user_id: int,
# ):
#     # Step 1: Validate the QR token
#     qr_session = validate_qr_token(
#         db=db,
#         raw_token=raw_qr_token
#     )

#     if qr_session is None:
#         raise ValueError("Invalid or expired QR code")

#     # Step 2: Get current date and time
#     current_datetime = get_current_india_datetime()
#     current_date = current_datetime.date()

#     # Step 3: Check whether this employee already
#     # has an attendance record for today
#     attendance = (
#         db.query(Attendance)
#         .filter(
#             Attendance.employee_id == employee.id,
#             Attendance.attendance_date == current_date
#         )
#         .first()
#     )

#     # Step 4: Prevent duplicate check-in
#     if attendance is not None:

#         # Employee is already inside
#         if (
#             attendance.check_in is not None
#             and attendance.check_out is None
#         ):
#             raise ValueError(
#                 "Employee is already checked in"
#             )

#         # Employee already completed today's attendance
#         if (
#             attendance.check_in is not None
#             and attendance.check_out is not None
#         ):
#             raise ValueError(
#                 "Employee has already completed attendance for today"
#             )

#     # Step 5: Determine whether employee is late
#     late_time = time(9, 15)

#     is_late = current_datetime.time() > late_time

#     # Step 6: Create attendance record
#     attendance = Attendance(
#         employee_id=employee.id,
#         attendance_date=current_date,
#         check_in=current_datetime,
#         status="INSIDE",
#         is_late=is_late,
#         check_in_qr_id=qr_session.id
#     )

#     # Step 7: Save to PostgreSQL
#     db.add(attendance)
#     db.commit()
#     db.refresh(attendance)

#     # Step 8: Create audit log
#     create_audit_log(
#         db=db,
#         user_id=user_id,
#         action="CHECK_IN",
#     )

#     # Step 9: Return the created attendance
#     return attendance


# def check_out_employee(
#     db: Session,
#     employee: Employee,
#     raw_qr_token: str,
#     user_id: int,
# ):
#     # Step 1: Validate the QR token
#     qr_session = validate_qr_token(
#         db=db,
#         raw_token=raw_qr_token
#     )

#     if qr_session is None:
#         raise ValueError("Invalid or expired QR code")

#     # Step 2: Get current date and time
#     current_datetime = get_current_india_datetime()
#     current_date = current_datetime.date()

#     # Step 3: Find today's attendance record
#     attendance = (
#         db.query(Attendance)
#         .filter(
#             Attendance.employee_id == employee.id,
#             Attendance.attendance_date == current_date
#         )
#         .first()
#     )

#     # Step 4: Make sure a check-in exists
#     if attendance is None:
#         raise ValueError(
#             "No check-in record found for today"
#         )

#     # Step 5: Prevent duplicate check-out
#     if attendance.check_out is not None:
#         raise ValueError(
#             "Employee has already checked out"
#         )

#     # Step 6: Make sure the employee is currently inside
#     if attendance.check_in is None:
#         raise ValueError(
#             "Employee has not checked in"
#         )

#     # Step 7: Record check-out time
#     attendance.check_out = current_datetime

#     # Step 8: Calculate working time
#     working_seconds = (
#         attendance.check_out - attendance.check_in
#     ).total_seconds()

#     working_minutes = int(
#         working_seconds / 60
#     )

#     attendance.working_minutes = working_minutes

#     # Step 9: Update attendance status
#     attendance.status = "OUTSIDE"

#     # Step 10: Store the QR session used for check-out
#     attendance.check_out_qr_id = qr_session.id

#     # Step 11: Save changes
#     db.commit()
#     db.refresh(attendance)

#     # Step 12: Create audit log
#     create_audit_log(
#         db=db,
#         user_id=user_id,
#         action="CHECK_OUT",
#     )

#     return attendance


# def get_employee_attendance_history(
#     db: Session,
#     employee: Employee
# ):
#     attendance_records = (
#         db.query(Attendance)
#         .filter(
#             Attendance.employee_id == employee.id
#         )
#         .order_by(
#             Attendance.attendance_date.desc()
#         )
#         .all()
#     )

#     return attendance_records


# def get_all_attendance(
#     db: Session
# ):
#     attendance_records = (
#         db.query(Attendance)
#         .order_by(
#             Attendance.attendance_date.desc(),
#             Attendance.id.desc()
#         )
#         .all()
#     )

#     return attendance_records














from datetime import datetime, time

from sqlalchemy.orm import Session

from app.core.timezone import (
    INDIA_TIMEZONE,
    get_current_india_datetime,
)
from app.database.models import Attendance, Employee
from app.services.qr_service import validate_qr_token
from app.services.audit_service import create_audit_log


def normalize_india_datetime(value: datetime) -> datetime:
    """
    Convert an aware datetime to India time and remove timezone information.

    If the datetime is already naive, it is assumed to already
    represent India local time.
    """

    if value.tzinfo is not None:
        return value.astimezone(
            INDIA_TIMEZONE
        ).replace(tzinfo=None)

    return value


def check_in_employee(
    db: Session,
    employee: Employee,
    raw_qr_token: str,
    user_id: int,
):
    # Step 1: Validate the QR token
    qr_session = validate_qr_token(
        db=db,
        raw_token=raw_qr_token,
    )

    if qr_session is None:
        raise ValueError("Invalid or expired QR code")

    # Step 2: Get current India date and time
    current_datetime = get_current_india_datetime()
    current_date = current_datetime.date()

    # Step 3: Check whether this employee already
    # has an attendance record for today
    attendance = (
        db.query(Attendance)
        .filter(
            Attendance.employee_id == employee.id,
            Attendance.attendance_date == current_date,
        )
        .first()
    )

    # Step 4: Prevent duplicate check-in
    if attendance is not None:

        # Employee is already inside
        if (
            attendance.check_in is not None
            and attendance.check_out is None
        ):
            raise ValueError(
                "Employee is already checked in"
            )

        # Employee already completed today's attendance
        if (
            attendance.check_in is not None
            and attendance.check_out is not None
        ):
            raise ValueError(
                "Employee has already completed attendance for today"
            )

    # Step 5: Determine whether employee is late
    late_time = time(9, 15)

    is_late = current_datetime.time() > late_time

    # Step 6: Create attendance record
    attendance = Attendance(
        employee_id=employee.id,
        attendance_date=current_date,
        check_in=current_datetime,
        status="INSIDE",
        is_late=is_late,
        check_in_qr_id=qr_session.id,
    )

    # Step 7: Save to PostgreSQL
    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    # Step 8: Create audit log
    create_audit_log(
        db=db,
        user_id=user_id,
        action="CHECK_IN",
    )

    # Step 9: Return the created attendance
    return attendance


def check_out_employee(
    db: Session,
    employee: Employee,
    raw_qr_token: str,
    user_id: int,
):
    # Step 1: Validate the QR token
    qr_session = validate_qr_token(
        db=db,
        raw_token=raw_qr_token,
    )

    if qr_session is None:
        raise ValueError("Invalid or expired QR code")

    # Step 2: Get current India date and time
    current_datetime = get_current_india_datetime()
    current_date = current_datetime.date()

    # Step 3: Find today's attendance record
    attendance = (
        db.query(Attendance)
        .filter(
            Attendance.employee_id == employee.id,
            Attendance.attendance_date == current_date,
        )
        .first()
    )

    # Step 4: Make sure a check-in exists
    if attendance is None:
        raise ValueError(
            "No check-in record found for today"
        )

    # Step 5: Prevent duplicate check-out
    if attendance.check_out is not None:
        raise ValueError(
            "Employee has already checked out"
        )

    # Step 6: Make sure the employee is currently inside
    if attendance.check_in is None:
        raise ValueError(
            "Employee has not checked in"
        )

    # Step 7: Normalize both datetimes
    # This prevents the naive/aware datetime error.
    check_in_time = normalize_india_datetime(
        attendance.check_in
    )

    check_out_time = normalize_india_datetime(
        current_datetime
    )

    # Step 8: Record check-out time
    attendance.check_out = check_out_time

    # Step 9: Calculate working time
    working_seconds = (
        check_out_time - check_in_time
    ).total_seconds()

    working_minutes = int(
        working_seconds / 60
    )

    # Step 10: Store working minutes
    attendance.working_minutes = working_minutes

    # Step 11: Update attendance status
    attendance.status = "OUTSIDE"

    # Step 12: Store the QR session used for check-out
    attendance.check_out_qr_id = qr_session.id

    # Step 13: Save changes
    db.commit()
    db.refresh(attendance)

    # Step 14: Create audit log
    create_audit_log(
        db=db,
        user_id=user_id,
        action="CHECK_OUT",
    )

    # Step 15: Return updated attendance
    return attendance


def get_employee_attendance_history(
    db: Session,
    employee: Employee,
):
    attendance_records = (
        db.query(Attendance)
        .filter(
            Attendance.employee_id == employee.id
        )
        .order_by(
            Attendance.attendance_date.desc()
        )
        .all()
    )

    return attendance_records


def get_all_attendance(
    db: Session,
):
    attendance_records = (
        db.query(Attendance)
        .order_by(
            Attendance.attendance_date.desc(),
            Attendance.id.desc(),
        )
        .all()
    )

    return attendance_records