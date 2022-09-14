from typing import Any
from pydantic import BaseModel

class Video(BaseModel):
    id: int
    data: dict[str, Any]
    class Config:
        orm_mode = True
