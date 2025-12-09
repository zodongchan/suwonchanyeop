from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DiaryCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)               

class DiaryUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = Field(None, min_length=1)

class DiaryResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True