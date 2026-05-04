import aiosqlite
from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse

from database import get_db

router = APIRouter(tags=["comments"])


@router.post("/posts/{post_id}/comments")
async def create_comment(
    post_id: int,
    content: str = Form(...),
    author_id: str = Form(...),
    author_password: str = Form(...),
    db: aiosqlite.Connection = Depends(get_db),
):
    async with db.execute("SELECT id FROM posts WHERE id = ?", (post_id,)) as cursor:
        row = await cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

    await db.execute(
        "INSERT INTO comments (post_id, content, author_id, author_password) VALUES (?, ?, ?, ?)",
        (post_id, content, author_id, author_password),
    )
    await db.commit()
    return RedirectResponse(url=f"/posts/{post_id}", status_code=303)


@router.post("/comments/{comment_id}/delete")
async def delete_comment(
    comment_id: int,
    password: str = Form(...),
    db: aiosqlite.Connection = Depends(get_db),
):
    async with db.execute(
        "SELECT author_password FROM comments WHERE id = ?", (comment_id,)
    ) as cursor:
        row = await cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")

    if password != dict(row)["author_password"]:
        return JSONResponse(status_code=403, content={"detail": "비밀번호가 틀렸습니다."})

    await db.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
    await db.commit()
    return {"ok": True}
