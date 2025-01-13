from pydantic import BaseModel
from datetime import datetime

class Version(BaseModel):
    id: int
    prompt_id: int
    content: str
    version_number: int
    created_at: datetime

    class Config:
        from_attributes = True 