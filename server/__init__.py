from typing import List, Optional
import aiosqlite
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles
from .posts import Post


SQLITE_CONNECTION: Optional[aiosqlite.Connection] = None

async def get_sqlite_connection():
    global SQLITE_CONNECTION
    if SQLITE_CONNECTION is None:
        SQLITE_CONNECTION = await aiosqlite.connect(":memory:")
        SQLITE_CONNECTION.row_factory = aiosqlite.Row

        await (await SQLITE_CONNECTION.execute("""--sql
            CREATE TABLE IF NOT EXISTS posts (
                uid INTEGER PRIMARY KEY,
                title VARCHAR(256),
                content TEXT
            );
        """)).close()

        await (await SQLITE_CONNECTION.execute("""--sql
            INSERT INTO posts (title, content) VALUES
                ('Post 1', 'Content 1'),
                ('Post 2', 'Content 2'),
                ('Post 3', 'Content 3')
            ;
        """, ())).close()

        await SQLITE_CONNECTION.commit()

    return SQLITE_CONNECTION


app = FastAPI()


@app.on_event("shutdown")
async def on_shutdown():
    if SQLITE_CONNECTION is not None:
        await SQLITE_CONNECTION.close()


@app.get("/posts/{uid}", response_model=Post)
async def get_post(uid: int) -> Post:
    conn = await get_sqlite_connection()
    async with conn.execute(
        "SELECT uid, title, content FROM posts WHERE uid=?",
        (uid,)
    ) as cursor:
        row = await cursor.fetchone()
        if row is None:
            raise HTTPException(404, f"Post with uid={uid} not found")
        return Post(uid=row["uid"], title=row["title"], content=row["content"])



@app.get("/posts/", response_model=List[Post])
async def index_posts() -> List[Post]:
    conn = await get_sqlite_connection()
    async with conn.execute(
        "SELECT uid, title, content FROM posts"
    ) as cursor:
        posts = []
        async for row in cursor:
            post = Post(uid=row["uid"], title=row["title"], content=row["content"])
            posts.append(post)
        return posts


app.mount("/", StaticFiles(directory="frontend/public"))