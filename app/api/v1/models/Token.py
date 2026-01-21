from pydantic import BaseModel, ConfigDict, Field

class TokenModel(BaseModel):
    refresh_token: str = Field(
        ...,
        description="Authentication token",
        json_schema_extra={"example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."},
    )

    model_config = ConfigDict(
        extra="forbid",
    )


