# from datetime import date, datetime

# from pydantic import BaseModel, ConfigDict


# class EmployeeCreate(BaseModel):
#     employee_code: str
#     name: str
#     email: str
#     phone: str | None = None
#     department_id: int | None = None
#     designation: str | None = None
#     joining_date: date | None = None


# class EmployeeUpdate(BaseModel):
#     name: str | None = None
#     email: str | None = None
#     phone: str | None = None
#     department_id: int | None = None
#     designation: str | None = None
#     joining_date: date | None = None
#     status: str | None = None


# class EmployeeResponse(BaseModel):
#     id: int
#     employee_code: str
#     name: str
#     email: str
#     phone: str | None
#     department_id: int | None
#     designation: str | None
#     joining_date: date | None
#     status: str
#     created_at: datetime

#     model_config = ConfigDict(from_attributes=True)






from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr


class EmployeeCreate(BaseModel):
    employee_code: str
    username: str
    password: str
    name: str
    email: EmailStr
    phone: str | None = None
    department_id: int | None = None
    designation: str | None = None
    joining_date: date | None = None


class EmployeeUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    department_id: int | None = None
    designation: str | None = None
    joining_date: date | None = None
    status: str | None = None


class EmployeeResponse(BaseModel):
    id: int
    employee_code: str
    user_id: int | None
    name: str
    email: str
    phone: str | None
    department_id: int | None
    designation: str | None
    joining_date: date | None
    status: str

    model_config = ConfigDict(from_attributes=True)