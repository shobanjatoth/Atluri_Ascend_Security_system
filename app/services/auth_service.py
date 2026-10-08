# from sqlalchemy.orm import Session
# from app.services.audit_service import create_audit_log
# from app.database.models import User
# from app.core.security import (
#     verify_password,
#     create_access_token
# )


# def authenticate_user(
#     db: Session,
#     username: str,
#     password: str
# ):
#     """
#     Find the user and verify the supplied password.
#     """

#     user = (
#         db.query(User)
#         .filter(User.username == username)
#         .first()
#     )

#     if user is None:
#         return None

#     if not user.is_active:
#         return None

#     if not verify_password(
#         password,
#         user.password_hash
#     ):
#         return None

#     return user


# def generate_login_token(user: User) -> str:
#     """
#     Generate JWT for an authenticated user.
#     """

#     return create_access_token(
#         user_id=user.id,
#         username=user.username,
#         role=user.role
#     )

# create_audit_log(
#     db=db,
#     user_id=user.id,
#     action="LOGIN",
# )






# from sqlalchemy.orm import Session

# from app.database.models import User
# from app.core.security import (
#     verify_password,
#     create_access_token,
# )
# from app.services.audit_service import create_audit_log


# def authenticate_user(
#     db: Session,
#     username: str,
#     password: str,
# ):
#     """
#     Find the user and verify the supplied password.
#     """

#     user = (
#         db.query(User)
#         .filter(User.username == username)
#         .first()
#     )

#     if user is None:
#         return None

#     if not user.is_active:
#         return None

#     if not verify_password(
#         password,
#         user.password_hash,
#     ):
#         return None

#     return user


# def generate_login_token(
#     db: Session,
#     user: User,
# ) -> str:
#     """
#     Generate JWT for an authenticated user
#     and create an audit log.
#     """

#     token = create_access_token(
#         user_id=user.id,
#         username=user.username,
#         role=user.role,
#     )

#     create_audit_log(
#         db=db,
#         user_id=user.id,
#         action="LOGIN",
#     )

#     return token






from sqlalchemy.orm import Session

from app.database.models import User
from app.core.security import (
    verify_password,
    create_access_token,
)
from app.services.audit_service import create_audit_log


def authenticate_user(
    db: Session,
    username: str,
    password: str,
):
    user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if user is None:
        return None

    if not user.is_active:
        return None

    if not verify_password(
        password,
        user.password_hash,
    ):
        return None

    return user


def generate_login_token(
    db: Session,
    user: User,
) -> str:

    token = create_access_token(
        user_id=user.id,
        username=user.username,
        role=user.role,
    )

    create_audit_log(
        db=db,
        user_id=user.id,
        action="LOGIN",
    )

    return token