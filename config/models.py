from typing import List
from pydantic import BaseModel,Field, EmailStr


class User(BaseModel):
    user_id: int
    nombre: str
    email: EmailStr

class Type(BaseModel):
    type_id: int
    type: str
    subject: str
    message: str
    rate: int
    unit: str

class Sended(BaseModel):
    user_id: int
    type_id: int
    sended_at: int

class SendMail(BaseModel):
    email: EmailStr = Field(
        default=str, title="Notification Email", min_length=6, max_length=300,strict=True
    )
    type:int = Field(
        default=int, title="Type of Email", gt=0,strict=True
    )

class MailBody(BaseModel):
    to: EmailStr
    subject: str
    body: str