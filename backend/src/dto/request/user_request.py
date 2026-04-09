import re
from pydantic import BaseModel, EmailStr, Field, field_validator
from backend.src.domain.models.user import UserRole

USERNAME_PATTERN = re.compile(r'^[A-Za-zÀ-ÿ0-9._]+$')
PASSWORD_PATTERN = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
LETTERS_ONLY = re.compile(r'^[A-Za-zÀ-ÿ\s]+$')


class UserRequest(BaseModel):
    first_name: str = Field(..., min_length=3, max_length=25)
    last_name: str = Field(..., min_length=3, max_length=25)
    email: EmailStr = Field(...)
    username: str = Field(..., min_length=3, max_length=25)
    password: str = Field(..., min_length=8)
    role: UserRole = Field(UserRole.ADMIN)

    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not LETTERS_ONLY.match(value):
            raise ValueError("must contain only letters.")
        return value


    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not PASSWORD_PATTERN.match(value):
            raise ValueError(
                "password must contain at least one uppercase, one lowercase and one special character.")
        return value


    @field_validator('username')
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not USERNAME_PATTERN.match(value):
            raise ValueError("username must contain only letters, numbers, dots or underscores.")
        return value
