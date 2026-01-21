from pydantic import BaseModel, ConfigDict, Field, EmailStr, validator


class UserModel(BaseModel):
    user: str = Field(
        ...,
        description="Username",
        min_length=3,
        max_length=50,
        json_schema_extra={"example": "john_doe"},
    )

    email: EmailStr = Field(
        ...,
        description="Email address",
        min_length=6,
        max_length=100,
        json_schema_extra={"example": "john@example.com"},
    )

    password: str = Field(..., min_length=6, max_length=128)

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if len(v) > 128:
            raise ValueError("Password must be at most 128 characters long")
        return v

    @validator("user")
    def validate_username(cls, v):
        if len(v) < 3 or len(v) > 30:
            raise ValueError("Username must be between 3 and 30 characters long")
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError("Username must contain only letters, numbers, _ or -")
        return v.strip()

    model_config = ConfigDict(
        extra="forbid",
    )