from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    Id: int
    name: str
    email: EmailStr


class UserDB(UserSchema):
    Id: int


class UserList(BaseModel):
    users: list[UserPublic]
