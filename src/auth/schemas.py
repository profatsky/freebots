from pydantic import BaseModel, EmailStr, Field
from typing_extensions import Annotated

Password = Annotated[str, Field(min_length=8, max_length=32)]


class AuthCredentialsSchema(BaseModel):
    email: EmailStr
    password: Password
