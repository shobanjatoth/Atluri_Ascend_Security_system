# from datetime import datetime

# from pydantic import BaseModel, ConfigDict


# class QRGenerateResponse(BaseModel):
#     id: int
#     expires_at: datetime
#     location: str | None
#     qr_token: str

#     model_config = ConfigDict(from_attributes=True)




from datetime import datetime

from pydantic import BaseModel, ConfigDict




class QRGenerateResponse(BaseModel):
    id: int
    expires_at: datetime
    location: str | None
    qr_token: str

    model_config = ConfigDict(from_attributes=True)


class QRValidateRequest(BaseModel):
    qr_token: str


class QRValidateResponse(BaseModel):
    valid: bool
    message: str
    qr_session_id: int | None = None
    location: str | None = None
    expires_at: datetime | None = None