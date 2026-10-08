# from sqlalchemy.orm import Session

# from app.database.models import Department


# def create_department(
#     db: Session,
#     name: str
# ) -> Department:

#     existing_department = (
#         db.query(Department)
#         .filter(Department.name == name)
#         .first()
#     )

#     if existing_department:
#         raise ValueError("Department already exists")

#     department = Department(
#         name=name
#     )

#     db.add(department)
#     db.commit()
#     db.refresh(department)

#     return department


# def get_departments(
#     db: Session
# ):
#     return (
#         db.query(Department)
#         .order_by(Department.name.asc())
#         .all()
#     )


# def get_department_by_id(
#     db: Session,
#     department_id: int
# ):
#     return (
#         db.query(Department)
#         .filter(Department.id == department_id)
#         .first()
#     )



from sqlalchemy.orm import Session

from app.database.models import Department, Employee
from app.services.audit_service import create_audit_log


def create_department(
    db: Session,
    name: str,
    admin_user_id: int | None = None,
):
    # Remove unnecessary spaces
    name = name.strip()

    if not name:
        raise ValueError("Department name cannot be empty")

    # Check duplicate department
    existing_department = (
        db.query(Department)
        .filter(Department.name.ilike(name))
        .first()
    )

    if existing_department is not None:
        raise ValueError("Department already exists")

    department = Department(
        name=name,
    )

    db.add(department)
    db.commit()
    db.refresh(department)

    if admin_user_id is not None:
        create_audit_log(
            db=db,
            user_id=admin_user_id,
            action="DEPARTMENT_CREATED",
        )

    return department


def get_all_departments(db: Session):
    return (
        db.query(Department)
        .order_by(Department.name.asc())
        .all()
    )


def get_department_by_id(
    db: Session,
    department_id: int,
):
    return (
        db.query(Department)
        .filter(Department.id == department_id)
        .first()
    )


def update_department(
    db: Session,
    department: Department,
    name: str,
    admin_user_id: int | None = None,
):
    name = name.strip()

    if not name:
        raise ValueError("Department name cannot be empty")

    # Check whether another department already uses this name
    existing_department = (
        db.query(Department)
        .filter(
            Department.name.ilike(name),
            Department.id != department.id,
        )
        .first()
    )

    if existing_department is not None:
        raise ValueError("Department already exists")

    department.name = name

    db.commit()
    db.refresh(department)

    if admin_user_id is not None:
        create_audit_log(
            db=db,
            user_id=admin_user_id,
            action="DEPARTMENT_UPDATED",
        )

    return department


def delete_department(
    db: Session,
    department: Department,
    admin_user_id: int | None = None,
):
    # Check whether employees are still assigned
    employee_count = (
        db.query(Employee)
        .filter(Employee.department_id == department.id)
        .count()
    )

    if employee_count > 0:
        raise ValueError(
            "Cannot delete department because employees are assigned to it"
        )

    db.delete(department)
    db.commit()

    if admin_user_id is not None:
        create_audit_log(
            db=db,
            user_id=admin_user_id,
            action="DEPARTMENT_DELETED",
        )

    return True