from getpass import getpass

from app.database.connection import SessionLocal
from app.database.models import User
from app.core.security import hash_password


def reset_admin_password():
    db = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.username == "admin")
            .first()
        )

        if user is None:
            print("Admin user does not exist.")
            return

        new_password = getpass("Enter new admin password: ")

        if not new_password:
            print("Password cannot be empty.")
            return

        user.password_hash = hash_password(new_password)

        db.commit()

        print("Admin password updated successfully.")

    except Exception as e:
        db.rollback()
        print("Error:", e)

    finally:
        db.close()


if __name__ == "__main__":
    reset_admin_password()