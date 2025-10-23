from pydantic import BaseModel, EmailStr

class SignupSchema(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str
