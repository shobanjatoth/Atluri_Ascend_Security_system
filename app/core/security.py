# from datetime import datetime, timedelta, timezone
# from app.core.security import hash_password, verify_password
# from jose import JWTError, jwt
# from passlib.context import CryptContext

# from app.core.config import settings


# # ---------------------------------------------------------
# # Password hashing configuration
# # ---------------------------------------------------------

# pwd_context = CryptContext(
#     schemes=["bcrypt"],
#     deprecated="auto"
# )


# # ---------------------------------------------------------
# # Password functions
# # ---------------------------------------------------------

# def hash_password(password: str) -> str:
#     """
#     Convert a plain-text password into a secure bcrypt hash.
#     """

#     return pwd_context.hash(password)


# def verify_password(
#     plain_password: str,
#     hashed_password: str
# ) -> bool:
#     """
#     Compare a plain-text password with the stored hash.
#     """

#     return pwd_context.verify(
#         plain_password,
#         hashed_password
#     )


# # ---------------------------------------------------------
# # JWT creation
# # ---------------------------------------------------------

# def create_access_token(
#     user_id: int,
#     username: str,
#     role: str
# ) -> str:
#     """
#     Create a JWT access token for an authenticated user.
#     """

#     expire = datetime.now(timezone.utc) + timedelta(
#         minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
#     )

#     payload = {
#         "sub": str(user_id),
#         "username": username,
#         "role": role,
#         "exp": expire
#     }

#     token = jwt.encode(
#         payload,
#         settings.JWT_SECRET_KEY,
#         algorithm=settings.JWT_ALGORITHM
#     )

#     return token


# # ---------------------------------------------------------
# # JWT decoding
# # ---------------------------------------------------------

# def decode_access_token(token: str) -> dict | None:
#     """
#     Decode and validate a JWT token.

#     Returns:
#         dict -> valid token payload
#         None -> invalid/expired token
#     """

#     try:
#         payload = jwt.decode(
#             token,
#             settings.JWT_SECRET_KEY,
#             algorithms=[settings.JWT_ALGORITHM]
#         )

#         return payload

#     except JWTError:
#         return None





from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(
    user_id: int,
    username: str,
    role: str
) -> str:

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "username": username,
        "role": role,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token


def decode_access_token(
    token: str
) -> dict | None:

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        return payload

    except JWTError:
        return None