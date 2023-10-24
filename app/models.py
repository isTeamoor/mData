from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class Filters(BaseModel):
    filters: list




