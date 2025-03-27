from pydantic import BaseModel, EmailStr, HttpUrl


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    job_title: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    id: int


class User(UserBase):
    id: int
    avatar: HttpUrl

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    data: User


class UserDelete(BaseModel):
    id: int
