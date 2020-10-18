import asyncio
from typing import List, Optional
from pathlib import Path

import aiofiles
import aiosqlite
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles

import content_parser
from .posts import Post


###


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
                path VARCHAR(256)
            );
        """)).close()

        await (await SQLITE_CONNECTION.execute("""--sql
            INSERT INTO posts (title, path) VALUES
                ('Test post', 'test.clj')
            ;
        """, ())).close()

        await SQLITE_CONNECTION.commit()

    return SQLITE_CONNECTION


app = FastAPI()


@app.on_event("shutdown")
async def on_shutdown():
    if SQLITE_CONNECTION is not None:
        await SQLITE_CONNECTION.close()


###


async def load_post(uid: int, title: str, path: str) -> Optional[Post]:
    try:
        async with aiofiles.open(Path("store") / path) as file: # type: ignore
            content = await file.read()
            html = content_parser.html(content)
            return Post(uid=uid, title=title, content=html)
    except FileNotFoundError:
        return None


@app.get("/posts/{uid}", response_model=Post)
async def get_post(uid: int) -> Post:
    await asyncio.sleep(1)

    conn = await get_sqlite_connection()
    async with conn.execute(
        "SELECT uid, title, path FROM posts WHERE uid=?",
        (uid,)
    ) as cursor:
        row = await cursor.fetchone()
        if row is None:
            raise HTTPException(404, f"Post with uid={uid} not found")
        if (post := await load_post(row["uid"], row["title"], row["path"])) is None:
            raise HTTPException(404, f"Post with uid={uid} has an invalid path")
        return post



@app.get("/posts", response_model=List[Post])
async def index_posts() -> List[Post]:
    await asyncio.sleep(1)

    conn = await get_sqlite_connection()
    async with conn.execute(
        "SELECT uid, title, path FROM posts"
    ) as cursor:
        posts = []
        async for row in cursor:
            if post := await load_post(row["uid"], row["title"], row["path"]):
                posts.append(post)
        return posts


app.mount("/", StaticFiles(directory="frontend/public"))