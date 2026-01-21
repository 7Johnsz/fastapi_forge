from pydantic import BaseModel, ConfigDict, Field, EmailStr

class LoginModel(BaseModel):
    email: EmailStr = Field(
        ...,
        description="Email address",
        json_schema_extra={"example": "john@example.com"}
    )
    password: str = Field(..., min_length=6, max_length=128)
    
    model_config = ConfigDict(
        extra="forbid",
    )
