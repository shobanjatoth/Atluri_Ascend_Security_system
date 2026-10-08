import hashlib
import secrets
import io
# import qrcode
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.models import QRSession


def generate_qr_session(
    db: Session,
    location: str | None = None
) -> tuple[QRSession, str]:

    # Generate a random token.
    raw_token = secrets.token_urlsafe(32)

    # Store only the hash in the database.
    token_hash = hashlib.sha256(
        raw_token.encode("utf-8")
    ).hexdigest()

    generated_at = datetime.utcnow()

    expires_at = generated_at + timedelta(
        seconds=settings.QR_EXPIRATION_SECONDS
    )

    # Deactivate previous QR sessions.
    db.query(QRSession).filter(
        QRSession.is_active == True
    ).update(
        {"is_active": False},
        synchronize_session=False
    )

    qr_session = QRSession(
        token_hash=token_hash,
        location=location,
        generated_at=generated_at,
        expires_at=expires_at,
        is_active=True
    )

    db.add(qr_session)
    db.commit()
    db.refresh(qr_session)

    return qr_session, raw_token


def validate_qr_token(
    db: Session,
    raw_token: str
) -> QRSession | None:

    token_hash = hashlib.sha256(
        raw_token.encode("utf-8")
    ).hexdigest()

    qr_session = (
        db.query(QRSession)
        .filter(
            QRSession.token_hash == token_hash,
            QRSession.is_active == True
        )
        .first()
    )

    if qr_session is None:
        return None

    current_time = datetime.utcnow()

    if current_time >= qr_session.expires_at:
        qr_session.is_active = False
        db.commit()
        return None

    return qr_session


# def create_qr_image(raw_token: str) -> io.BytesIO:
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_M,
#         box_size=10,
#         border=4
#     )

#     qr.add_data(raw_token)
#     qr.make(fit=True)

#     image = qr.make_image()

#     image_buffer = io.BytesIO()

#     image.save(
#         image_buffer,
#         format="PNG"
#     )

#     image_buffer.seek(0)

#     return image_buffer