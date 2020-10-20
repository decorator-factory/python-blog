from typing import Optional
from pydantic import BaseModel


class Post(BaseModel):
    uid: int
    title: str
    content: Optional[str]
