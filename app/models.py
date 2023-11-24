from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class Selection(BaseModel):
    filters: list
    sections: list



