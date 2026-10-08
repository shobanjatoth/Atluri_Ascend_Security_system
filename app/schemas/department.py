# from datetime import datetime

# from pydantic import BaseModel, ConfigDict


# class DepartmentCreate(BaseModel):
#     name: str


# class DepartmentResponse(BaseModel):
#     id: int
#     name: str
#     created_at: datetime

#     model_config = ConfigDict(from_attributes=True)



from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DepartmentCreate(BaseModel):
    name: str


class DepartmentUpdate(BaseModel):
    name: str


class DepartmentResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)