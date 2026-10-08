# from sqlalchemy.orm import Session

# from app.database.models import AuditLog


# def create_audit_log(
#     db: Session,
#     user_id: int | None,
#     action: str,
#     ip_address: str | None = None,
#     device_info: str | None = None,
# ):
#     audit_log = AuditLog(
#         user_id=user_id,
#         action=action,
#         ip_address=ip_address,
#         device_info=device_info,
#     )

#     db.add(audit_log)
#     db.commit()
#     db.refresh(audit_log)

#     return audit_log


# def get_audit_logs(
#     db: Session,
#     limit: int = 100,
# ):
#     return (
#         db.query(AuditLog)
#         .order_by(AuditLog.created_at.desc())
#         .limit(limit)
#         .all()
#     )



from sqlalchemy.orm import Session

from app.database.models import AuditLog


def create_audit_log(
    db: Session,
    user_id: int | None,
    action: str,
    ip_address: str | None = None,
    device_info: str | None = None,
):
    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        ip_address=ip_address,
        device_info=device_info,
    )

    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)

    return audit_log


def get_audit_logs(
    db: Session,
    limit: int = 100,
):
    return (
        db.query(AuditLog)
        .order_by(AuditLog.created_at.desc())
        .limit(limit)
        .all()
    )