# from sqlalchemy.orm import Session

# from app.database.models import Attendance, Employee, Department


# def get_attendance_report(db: Session):
#     records = (
#         db.query(
#             Attendance,
#             Employee,
#             Department,
#         )
#         .join(
#             Employee,
#             Attendance.employee_id == Employee.id,
#         )
#         .outerjoin(
#             Department,
#             Employee.department_id == Department.id,
#         )
#         .order_by(
#             Attendance.attendance_date.desc(),
#             Attendance.id.desc(),
#         )
#         .all()
#     )

#     result = []

#     for attendance, employee, department in records:
#         result.append(
#             {
#                 "attendance_id": attendance.id,
#                 "employee_id": employee.id,
#                 "employee_name": employee.name,
#                 "employee_code": employee.employee_code,
#                 "department_name": (
#                     department.name
#                     if department is not None
#                     else None
#                 ),
#                 "attendance_date": attendance.attendance_date,
#                 "check_in": attendance.check_in,
#                 "check_out": attendance.check_out,
#                 "working_minutes": attendance.working_minutes,
#                 "status": attendance.status,
#                 "is_late": attendance.is_late,
#             }
#         )

#     return {
#         "total_records": len(result),
#         "records": result,
#     }





import csv
from io import BytesIO, StringIO
from openpyxl import Workbook
from datetime import date

from sqlalchemy.orm import Session

from app.database.models import Attendance, Employee, Department


def get_attendance_report(
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None,
    employee_id: int | None = None,
    department_id: int | None = None,
):
    query = (
        db.query(
            Attendance,
            Employee,
            Department,
        )
        .join(
            Employee,
            Attendance.employee_id == Employee.id,
        )
        .outerjoin(
            Department,
            Employee.department_id == Department.id,
        )
    )

    if start_date is not None:
        query = query.filter(
            Attendance.attendance_date >= start_date
        )

    if end_date is not None:
        query = query.filter(
            Attendance.attendance_date <= end_date
        )

    if employee_id is not None:
        query = query.filter(
            Attendance.employee_id == employee_id
        )

    if department_id is not None:
        query = query.filter(
            Employee.department_id == department_id
        )

    records = (
        query
        .order_by(
            Attendance.attendance_date.desc(),
            Attendance.id.desc(),
        )
        .all()
    )

    result = []

    for attendance, employee, department in records:
        result.append(
            {
                "attendance_id": attendance.id,
                "employee_id": employee.id,
                "employee_name": employee.name,
                "employee_code": employee.employee_code,
                "department_name": (
                    department.name
                    if department is not None
                    else None
                ),
                "attendance_date": attendance.attendance_date,
                "check_in": attendance.check_in,
                "check_out": attendance.check_out,
                "working_minutes": attendance.working_minutes,
                "status": attendance.status,
                "is_late": attendance.is_late,
            }
        )

    return {
        "total_records": len(result),
        "records": result,
    }
    
    


def create_csv_report(records):
    output = StringIO()

    writer = csv.writer(output)

    writer.writerow(
        [
            "Attendance ID",
            "Employee ID",
            "Employee Name",
            "Employee Code",
            "Department",
            "Attendance Date",
            "Check In",
            "Check Out",
            "Working Minutes",
            "Status",
            "Late",
        ]
    )

    for record in records:
        writer.writerow(
            [
                record["attendance_id"],
                record["employee_id"],
                record["employee_name"],
                record["employee_code"],
                record["department_name"],
                record["attendance_date"],
                record["check_in"],
                record["check_out"],
                record["working_minutes"],
                record["status"],
                record["is_late"],
            ]
        )

    return output.getvalue()


def create_excel_report(records):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Attendance Report"

    headers = [
        "Attendance ID",
        "Employee ID",
        "Employee Name",
        "Employee Code",
        "Department",
        "Attendance Date",
        "Check In",
        "Check Out",
        "Working Minutes",
        "Status",
        "Late",
    ]

    worksheet.append(headers)

    for record in records:
        worksheet.append(
            [
                record["attendance_id"],
                record["employee_id"],
                record["employee_name"],
                record["employee_code"],
                record["department_name"],
                record["attendance_date"],
                record["check_in"],
                record["check_out"],
                record["working_minutes"],
                record["status"],
                record["is_late"],
            ]
        )

    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    return output