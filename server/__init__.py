import json
import asyncio
import watchgod
from typing import List, Optional
from pathlib import Path

import aiofiles
import aiosqlite
import sqlite3
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
        aiosqlite.register_adapter(list, json.dumps)

        def parse_list(s: bytes) -> list:
            result = json.loads(s)
            if not isinstance(result, list):
                raise TypeError(f"{result} is not a list")
            return result
        aiosqlite.register_converter("ARRAY", parse_list)

        SQLITE_CONNECTION = await aiosqlite.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
        SQLITE_CONNECTION.row_factory = aiosqlite.Row

    return SQLITE_CONNECTION


async def setup_sqlite_from_config():
    # The configuration file stores the information about the posts
    # This data is loaded into an in-memory SQLite database
    # for convenient and performant searching

    conn = await get_sqlite_connection()
    await (await conn.execute("""
        --sql
        DROP TABLE IF EXISTS posts;
    """)).close()

    await (await conn.execute("""
        --sql
        CREATE TABLE IF NOT EXISTS posts (
            uid INTEGER PRIMARY KEY,
            title VARCHAR(256),
            content TEXT,
            position INTEGER,
            tags ARRAY
        );
    """)).close()
    await conn.commit()

    async with aiofiles.open(Path("store/store.json")) as config:  # type: ignore
        data = json.loads(await config.read())
        for i, post in enumerate(data["posts"]):
            async with aiofiles.open(Path("store") / post["path"]) as file:  # type: ignore
                content = content_parser.html(await file.read())
            cursor = await conn.execute("""--sql
                INSERT INTO posts (uid, title, content, tags, position) VALUES (?, ?, ?, ?, ?);
            """, (post["uid"], post["title"], content, post["tags"], i))
            await cursor.close()
    await conn.commit()



app = FastAPI()


async def reload_sqlite():
    global SQLITE_CONNECTION
    try:
        await setup_sqlite_from_config()
    except:
        if SQLITE_CONNECTION is not None:
            await SQLITE_CONNECTION.close()
            SQLITE_CONNECTION = None
        raise


async def live_reload():
    async for _ in watchgod.awatch("store/"):
        print("Live reloading the store...")
        try:
            await reload_sqlite()
        except Exception as e:
            print(e.__class__.__name__, e)


@app.on_event("startup")
async def on_startup():
    await reload_sqlite()
    asyncio.create_task(live_reload())




@app.on_event("shutdown")
async def on_shutdown():
    if SQLITE_CONNECTION is not None:
        await SQLITE_CONNECTION.close()


###


@app.get("/posts/{uid}", response_model=Post)
async def get_post(uid: int) -> Post:
    conn = await get_sqlite_connection()
    async with conn.execute(
        "SELECT uid, title, tags, content FROM posts WHERE uid=?",
        (uid,)
    ) as cursor:
        row = await cursor.fetchone()
        if row is None:
            raise HTTPException(404, f"Post with uid={uid} not found")
        return Post(uid=row["uid"], title=row["title"], content=row["content"], tags=row["tags"])



@app.get("/posts", response_model=List[Post])
async def index_posts(include_content: Optional[bool] = None) -> List[Post]:
    conn = await get_sqlite_connection()
    if include_content:
        async with conn.execute("SELECT uid, title, tags, content FROM posts ORDER BY position") as cursor:
            posts = []
            async for row in cursor:
                post = Post(uid=row["uid"], title=row["title"], content=row["content"], tags=row["tags"])
                posts.append(post)
            return posts
    else:
        async with conn.execute("SELECT uid, title, tags FROM posts ORDER BY position") as cursor:
            posts = []
            async for row in cursor:
                post = Post(uid=row["uid"], title=row["title"], content=None, tags=row["tags"])
                posts.append(post)
            return posts


@app.get("/posts/{uid}/content", response_model=str)
async def get_post_content(uid: int) -> str:
    conn = await get_sqlite_connection()
    async with conn.execute(
        "SELECT content FROM posts WHERE uid = ?",
        (uid,)
    ) as cursor:
        row = await cursor.fetchone()
        if row is None:
            raise HTTPException(404, f"Post with uid={uid} not found")
        return row["content"]


app.mount("/", StaticFiles(directory="frontend/public"))
