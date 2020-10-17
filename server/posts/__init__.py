from pydantic import BaseModel


class Post(BaseModel):
    uid: int
    title: str
    content: str