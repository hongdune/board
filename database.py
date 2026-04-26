import aiosqlite

DB_PATH = "board.db"


async def get_db():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        yield db


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                title            TEXT NOT NULL,
                content          TEXT NOT NULL,
                author_id        TEXT NOT NULL,
                author_password  TEXT NOT NULL,
                image_url        TEXT,
                created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()


async def reset_db(): # 클로드 사용 없이 DB 초기화 목적으로 별도 추가
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM comments")
        await db.execute("DELETE FROM posts")
        await db.commit()