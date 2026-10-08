from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import User, Employee
from app.core.security import hash_password


def create_employee_user():
    db: Session = SessionLocal()

    try:
        employee = (
            db.query(Employee)
            .filter(Employee.employee_code == "EMP001")
            .first()
        )

        if employee is None:
            print("Employee EMP001 not found.")
            return

        existing_user = (
            db.query(User)
            .filter(User.username == "rahul")
            .first()
        )

        if existing_user:
            user = existing_user
            print("User 'rahul' already exists.")
        else:
            user = User(
                username="rahul",
                password_hash=hash_password("Rahul@123"),
                role="EMPLOYEE",
                is_active=True
            )

            db.add(user)
            db.flush()

            print("Employee user created.")

        employee.user_id = user.id
        employee.status = "ACTIVE"

        db.commit()
        db.refresh(employee)

        print("Employee account linked successfully.")
        print(f"Employee ID : {employee.id}")
        print(f"User ID     : {user.id}")
        print(f"Username    : {user.username}")
        print(f"Status      : {employee.status}")

    finally:
        db.close()


if __name__ == "__main__":
    create_employee_user()