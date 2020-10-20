from typing import List, Optional
from pydantic import BaseModel


class Post(BaseModel):
    uid: int
    title: str
    tags: List[str]
    content: Optional[str]
