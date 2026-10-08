# from datetime import date, datetime

# from pydantic import BaseModel


# class AttendanceReportItem(BaseModel):
#     attendance_id: int
#     employee_id: int
#     employee_name: str
#     employee_code: str
#     department_name: str | None
#     attendance_date: date
#     check_in: datetime | None
#     check_out: datetime | None
#     working_minutes: int | None
#     status: str | None
#     is_late: bool


# class AttendanceReportResponse(BaseModel):
#     total_records: int
#     records: list[AttendanceReportItem]



from datetime import date, datetime

from pydantic import BaseModel


class AttendanceReportItem(BaseModel):
    attendance_id: int
    employee_id: int
    employee_name: str
    employee_code: str
    department_name: str | None
    attendance_date: date
    check_in: datetime | None
    check_out: datetime | None
    working_minutes: int | None
    status: str | None
    is_late: bool


class AttendanceReportResponse(BaseModel):
    total_records: int
    records: list[AttendanceReportItem]