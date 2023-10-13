from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class workOrders(BaseModel):
    email: EmailStr
    password: str

class requisition(BaseModel):
    data: str
    extra: int


