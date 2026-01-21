from pydantic import BaseModel, ConfigDict, Field

class LogoutModel(BaseModel):
    token: str = Field(
        ...,
        description="JWT token for logout",
        json_schema_extra={"example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
    )
    
    model_config = ConfigDict(
        extra="forbid",
    )


