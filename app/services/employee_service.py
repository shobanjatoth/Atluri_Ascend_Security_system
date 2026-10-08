# from sqlalchemy.orm import Session

# from app.database.models import Employee


# def create_employee(
#     db: Session,
#     employee_code: str,
#     name: str,
#     email: str,
#     phone: str | None,
#     department_id: int | None,
#     designation: str | None,
#     joining_date
# ):
#     existing_code = (
#         db.query(Employee)
#         .filter(Employee.employee_code == employee_code)
#         .first()
#     )

#     if existing_code:
#         raise ValueError("Employee code already exists")

#     existing_email = (
#         db.query(Employee)
#         .filter(Employee.email == email)
#         .first()
#     )

#     if existing_email:
#         raise ValueError("Employee email already exists")

#     employee = Employee(
#         employee_code=employee_code,
#         name=name,
#         email=email,
#         phone=phone,
#         department_id=department_id,
#         designation=designation,
#         joining_date=joining_date,
#         status="ACTIVE"
#     )

#     db.add(employee)
#     db.commit()
#     db.refresh(employee)

#     return employee


# def get_employees(db: Session):
#     return (
#         db.query(Employee)
#         .order_by(Employee.id.desc())
#         .all()
#     )


# def get_employee_by_id(
#     db: Session,
#     employee_id: int
# ):
#     return (
#         db.query(Employee)
#         .filter(Employee.id == employee_id)
#         .first()
#     )


# def update_employee(
#     db: Session,
#     employee: Employee,
#     employee_data
# ):
#     if employee_data.name is not None:
#         employee.name = employee_data.name

#     if employee_data.email is not None:
#         existing_email = (
#             db.query(Employee)
#             .filter(
#                 Employee.email == employee_data.email,
#                 Employee.id != employee.id
#             )
#             .first()
#         )

#         if existing_email:
#             raise ValueError("Employee email already exists")

#         employee.email = employee_data.email

#     if employee_data.phone is not None:
#         employee.phone = employee_data.phone

#     if employee_data.department_id is not None:
#         employee.department_id = employee_data.department_id

#     if employee_data.designation is not None:
#         employee.designation = employee_data.designation

#     if employee_data.joining_date is not None:
#         employee.joining_date = employee_data.joining_date

#     if employee_data.status is not None:
#         employee.status = employee_data.status

#     db.commit()
#     db.refresh(employee)

#     return employee


# def deactivate_employee(
#     db: Session,
#     employee: Employee
# ):
#     employee.status = "INACTIVE"

#     db.commit()
#     db.refresh(employee)

#     return employee





from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.database.models import Employee, User
from app.services.audit_service import create_audit_log


def create_employee(
    db: Session,
    employee_code: str,
    username: str,
    password: str,
    name: str,
    email: str,
    phone: str | None = None,
    department_id: int | None = None,
    designation: str | None = None,
    joining_date=None,
    admin_user_id: int | None = None,
):
    # Check employee code
    existing_employee = (
        db.query(Employee)
        .filter(Employee.employee_code == employee_code)
        .first()
    )

    if existing_employee is not None:
        raise ValueError("Employee code already exists")

    # Check username
    existing_user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if existing_user is not None:
        raise ValueError("Username already exists")

    # Check email
    existing_email = (
        db.query(Employee)
        .filter(Employee.email == email)
        .first()
    )

    if existing_email is not None:
        raise ValueError("Email already exists")

    # Create login user
    user = User(
        username=username,
        password_hash=hash_password(password),
        role="EMPLOYEE",
        is_active=True,
    )

    db.add(user)
    db.flush()

    # Create employee
    employee = Employee(
        employee_code=employee_code,
        user_id=user.id,
        name=name,
        email=email,
        phone=phone,
        department_id=department_id,
        designation=designation,
        joining_date=joining_date,
        status="ACTIVE",
    )

    db.add(employee)
    db.commit()
    db.refresh(employee)

    # Audit
    if admin_user_id is not None:
        create_audit_log(
            db=db,
            user_id=admin_user_id,
            action="EMPLOYEE_CREATED",
        )

    return employee


def get_all_employees(db: Session):
    return (
        db.query(Employee)
        .order_by(Employee.id.desc())
        .all()
    )


def get_employee_by_id(
    db: Session,
    employee_id: int,
):
    return (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )


def update_employee(
    db: Session,
    employee: Employee,
    name: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    department_id: int | None = None,
    designation: str | None = None,
    joining_date=None,
    status: str | None = None,
    admin_user_id: int | None = None,
):
    if email is not None and email != employee.email:
        existing_email = (
            db.query(Employee)
            .filter(
                Employee.email == email,
                Employee.id != employee.id,
            )
            .first()
        )

        if existing_email is not None:
            raise ValueError("Email already exists")

        employee.email = email

    if name is not None:
        employee.name = name

    if phone is not None:
        employee.phone = phone

    if department_id is not None:
        employee.department_id = department_id

    if designation is not None:
        employee.designation = designation

    if joining_date is not None:
        employee.joining_date = joining_date

    if status is not None:
        if status not in ["ACTIVE", "INACTIVE"]:
            raise ValueError("Status must be ACTIVE or INACTIVE")

        employee.status = status

        # Keep login account status synchronized
        if employee.user is not None:
            employee.user.is_active = status == "ACTIVE"

    db.commit()
    db.refresh(employee)

    if admin_user_id is not None:
        create_audit_log(
            db=db,
            user_id=admin_user_id,
            action="EMPLOYEE_UPDATED",
        )

    return employee


def deactivate_employee(
    db: Session,
    employee: Employee,
    admin_user_id: int | None = None,
):
    employee.status = "INACTIVE"

    if employee.user is not None:
        employee.user.is_active = False

    db.commit()
    db.refresh(employee)

    if admin_user_id is not None:
        create_audit_log(
            db=db,
            user_id=admin_user_id,
            action="EMPLOYEE_DEACTIVATED",
        )

    return employee