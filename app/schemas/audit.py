from datetime import datetime

from pydantic import BaseModel


class AuditLogResponse(BaseModel):
    id: int
    user_id: int | None
    action: str
    ip_address: str | None
    device_info: str | None
    created_at: datetime