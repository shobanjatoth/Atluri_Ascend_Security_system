from datetime import date, datetime

from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    total_employees: int
    active_employees: int
    present_today: int
    currently_inside: int
    checked_out_today: int
    late_today: int


class DepartmentSummary(BaseModel):
    department_id: int
    department_name: str
    employee_count: int


class RecentAttendance(BaseModel):
    attendance_id: int
    employee_id: int
    employee_name: str
    employee_code: str
    attendance_date: date
    check_in: datetime | None
    check_out: datetime | None
    working_minutes: int | None
    status: str | None
    is_late: bool


class DashboardResponse(BaseModel):
    summary: DashboardSummaryResponse
    departments: list[DepartmentSummary]
    recent_attendance: list[RecentAttendance]