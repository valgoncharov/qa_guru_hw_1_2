from pydantic import BaseModel, EmailStr, HttpUrl


class UserData(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    job_title: str
    avatar: HttpUrl


class UserCreateData(BaseModel):
    email: str
    first_name: str
    last_name: str
    job_title: str


class UserResponse(BaseModel):
    data: UserData


class UserUpdateData(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    job_title: str


class UserDeleteData(BaseModel):
    id: int
