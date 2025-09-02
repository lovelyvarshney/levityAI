from typing import Optional
from pydantic import BaseModel, field_validator

class NotifyRequest(BaseModel):
    origin: str
    destination: str
    custom_max_delay_allowed: Optional[int] = None
    fallback_message: Optional[object] = {}
    channels: object
    mock_data: Optional[bool] = False

    # Custom field_validator
    @field_validator("origin", "destination")
    def must_not_be_empty(cls, value, field):
        if not value or not value.strip():
            raise ValueError(f"{field.name} must not be empty")
        return value
