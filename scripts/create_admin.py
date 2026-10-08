from getpass import getpass

from app.database.connection import SessionLocal
from app.database.models import User
from app.core.security import hash_password


def create_admin():
    db = SessionLocal()

    try:
        username = input("Enter admin username: ").strip()

        password = getpass("Enter admin password: ")

        existing_user = (
            db.query(User)
            .filter(User.username == username)
            .first()
        )

        if existing_user:
            print("User already exists.")
            return

        admin = User(
            username=username,
            password_hash=hash_password(password),
            role="ADMIN",
            is_active=True
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print()
        print("Admin user created successfully.")
        print(f"User ID : {admin.id}")
        print(f"Username: {admin.username}")
        print(f"Role    : {admin.role}")

    except Exception as e:
        db.rollback()
        print("Error creating admin:", e)

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
    
    
    
    
