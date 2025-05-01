from pydantic import BaseModel, ConfigDict

class BaseSchema(BaseModel):
    # This is a base schema that can be used to define common fields for other schemas
    
    model_config = ConfigDict(
        extra="forbid",
    )
    
    
    