from fastapi import FastAPI
from .posts import Post


app = FastAPI()


@app.get("/posts/{uid}", response_model=Post)
async def main(uid: int) -> Post:
    return Post(
        uid=uid,
        title="Title",
        content="Hello",
    )