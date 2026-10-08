from sqlalchemy.orm import Session

from app.core.timezone import get_current_india_date
from app.database.models import Attendance, Department, Employee


def get_dashboard_summary(db: Session):
    today = get_current_india_date()

    total_employees = (
        db.query(Employee)
        .count()
    )

    active_employees = (
        db.query(Employee)
        .filter(Employee.status == "ACTIVE")
        .count()
    )

    today_attendance = (
        db.query(Attendance)
        .filter(Attendance.attendance_date == today)
        .all()
    )

    present_today = len(today_attendance)

    currently_inside = 0
    checked_out_today = 0
    late_today = 0

    for attendance in today_attendance:
        if attendance.check_in is not None and attendance.check_out is None:
            currently_inside += 1

        if attendance.check_out is not None:
            checked_out_today += 1

        if attendance.is_late:
            late_today += 1

    return {
        "total_employees": total_employees,
        "active_employees": active_employees,
        "present_today": present_today,
        "currently_inside": currently_inside,
        "checked_out_today": checked_out_today,
        "late_today": late_today,
    }


def get_department_summary(db: Session):
    departments = (
        db.query(Department)
        .order_by(Department.name.asc())
        .all()
    )

    result = []

    for department in departments:
        employee_count = (
            db.query(Employee)
            .filter(
                Employee.department_id == department.id,
                Employee.status == "ACTIVE",
            )
            .count()
        )

        result.append(
            {
                "department_id": department.id,
                "department_name": department.name,
                "employee_count": employee_count,
            }
        )

    return result


def get_recent_attendance(db: Session, limit: int = 10):
    records = (
        db.query(Attendance)
        .join(Employee, Attendance.employee_id == Employee.id)
        .order_by(
            Attendance.attendance_date.desc(),
            Attendance.id.desc(),
        )
        .limit(limit)
        .all()
    )

    result = []

    for attendance in records:
        result.append(
            {
                "attendance_id": attendance.id,
                "employee_id": attendance.employee_id,
                "employee_name": attendance.employee.name,
                "employee_code": attendance.employee.employee_code,
                "attendance_date": attendance.attendance_date,
                "check_in": attendance.check_in,
                "check_out": attendance.check_out,
                "working_minutes": attendance.working_minutes,
                "status": attendance.status,
                "is_late": attendance.is_late,
            }
        )

    return result




def get_full_dashboard(db: Session):
    summary = get_dashboard_summary(db)

    departments = get_department_summary(db)

    recent_attendance = get_recent_attendance(db, limit=10)

    return {
        "summary": summary,
        "departments": departments,
        "recent_attendance": recent_attendance,
    }




from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.models import Attendance, Department, Employee


def get_dashboard_data(db: Session):
    today = date.today()

    total_employees = (
        db.query(Employee)
        .filter(Employee.status == "ACTIVE")
        .count()
    )

    total_departments = db.query(Department).count()

    checked_in_today = (
        db.query(Attendance)
        .filter(
            Attendance.attendance_date == today,
            Attendance.check_in.isnot(None),
            Attendance.check_out.is_(None),
        )
        .count()
    )

    checked_out_today = (
        db.query(Attendance)
        .filter(
            Attendance.attendance_date == today,
            Attendance.check_out.isnot(None),
        )
        .count()
    )

    late_today = (
        db.query(Attendance)
        .filter(
            Attendance.attendance_date == today,
            Attendance.is_late == True,
        )
        .count()
    )

    today_attendance = (
        db.query(Attendance)
        .filter(Attendance.attendance_date == today)
        .count()
    )

    absent_today = max(
        total_employees - today_attendance,
        0,
    )

    return {
        "total_employees": total_employees,
        "total_departments": total_departments,
        "checked_in_today": checked_in_today,
        "checked_out_today": checked_out_today,
        "late_today": late_today,
        "absent_today": absent_today,
    }