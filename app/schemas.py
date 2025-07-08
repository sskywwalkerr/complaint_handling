from typing import Optional, Dict

from pydantic import BaseModel
from datetime import datetime


class ComplaintCreate(BaseModel):
    text: str


class ComplaintResponse(BaseModel):
    id: int
    status: str
    sentiment: str
    category: str


class OpenComplaint(BaseModel):
    id: int
    text: str
    category: str
    sentiment: str
    timestamp: datetime
