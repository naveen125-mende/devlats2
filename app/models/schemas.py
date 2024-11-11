#app/models/schemas.py
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
class UserSchema(BaseModel):
    fullname: str
    email: EmailStr
    contact_number: int
    password: str
       

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

