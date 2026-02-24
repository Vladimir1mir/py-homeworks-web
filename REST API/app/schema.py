import uuid
from decimal import Decimal
from typing import Literal, Optional
from pydantic import BaseModel, constr, condecimal


class CreateAdvertisementRequest(BaseModel):
    title: constr(min_length=2, max_length=100)
    description: constr(min_length=10, max_length=500)
    price: condecimal(gt=0, max_digits=12, decimal_places=2)


class UpdateAdvertisementRequest(BaseModel):
    title: constr(min_length=2, max_length=100) | None = None
    description: constr(min_length=10, max_length=500) | None = None
    price: condecimal(gt=0, max_digits=12, decimal_places=2) | None = None


class GetAdvertisementResponse(BaseModel):
    title: str
    description: str
    price: Decimal
    creation_time: str
    user_id: int


class SearchAdvertisementResponse(BaseModel):
    results: list[GetAdvertisementResponse]


class CreateAdvertisementResponse(BaseModel):
    id: int


class SuccessResponse(BaseModel):
    status: Literal["success"]


class UpdateAdvertisementResponse(SuccessResponse):
    pass


class DeleteAdvertisementResponse(SuccessResponse):
    pass


class BaseUserRequest(BaseModel):
    name: constr(min_length=2, max_length=100)
    password: constr(min_length=8, max_length=100)
    role: Optional[str] = "user"


class LoginRequest(BaseUserRequest):
    pass


class LoginResponse(BaseModel):
    token: uuid.UUID


class CreateUserRequest(BaseUserRequest):
    pass


class CreateUserResponse(BaseModel):
    id: int


class UpdateUserRequest(CreateUserRequest):
    pass


class UpdateUserResponse(SuccessResponse):
    pass


class GetUserResponse(BaseModel):
    id: int
    name: str


class DeleteUserResponse(SuccessResponse):
    pass