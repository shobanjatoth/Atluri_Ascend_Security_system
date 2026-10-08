# from datetime import date, datetime

# from pydantic import BaseModel


# class CheckInRequest(BaseModel):
#     qr_token: str


# class CheckInResponse(BaseModel):
#     message: str
#     attendance_id: int
#     employee_id: int
#     attendance_date: date
#     check_in: datetime
#     status: str
#     is_late: bool



from datetime import date, datetime

from pydantic import BaseModel


class CheckInRequest(BaseModel):
    qr_token: str


class CheckInResponse(BaseModel):
    message: str
    attendance_id: int
    employee_id: int
    attendance_date: date
    check_in: datetime
    status: str
    is_late: bool


class CheckOutRequest(BaseModel):
    qr_token: str


class CheckOutResponse(BaseModel):
    message: str
    attendance_id: int
    employee_id: int
    attendance_date: date
    check_in: datetime
    check_out: datetime
    working_minutes: int
    status: str
    


class AttendanceHistoryResponse(BaseModel):
    id: int
    employee_id: int
    attendance_date: date
    check_in: datetime | None
    check_out: datetime | None
    working_minutes: int | None
    status: str | None
    is_late: bool
    
    
    
class AdminAttendanceResponse(BaseModel):
    id: int
    employee_id: int
    attendance_date: date
    check_in: datetime | None
    check_out: datetime | None
    working_minutes: int | None
    status: str | None
    is_late: bool