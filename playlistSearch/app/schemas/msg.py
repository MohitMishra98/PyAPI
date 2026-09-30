from typing import Optional
from pydantic import BaseModel


class Msg(BaseModel):
    message: str
    detail: Optional[str] = None
