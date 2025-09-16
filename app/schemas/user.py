from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    cpf: str
    phone_number: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    create_at: datetime
    is_active: bool

    class Config:
        from_attributes = True