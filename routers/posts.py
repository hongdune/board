from pathlib import Path
from typing import Optional

import aiosqlite
from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from database import get_db

router = APIRouter(prefix="/posts", tags=["posts"])
templates = Jinja2Templates(directory="templates")

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}
UPLOAD_DIR = Path("static/uploads")


def _check_extension(filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="허용되지 않는 이미지 형식입니다.")
    return ext


@router.get("")
async def list_posts(request: Request, db: aiosqlite.Connection = Depends(get_db)):
    async with db.execute(
        "SELECT * FROM posts ORDER BY created_at DESC"
    ) as cursor:
        posts = [dict(row) for row in await cursor.fetchall()]
    return templates.TemplateResponse(
        request=request, name="list.html", context={"posts": posts}
    )


@router.get("/new")
async def new_post_form(request: Request):
    return templates.TemplateResponse(request=request, name="post_create.html", context={})


@router.get("/{post_id}")
async def post_detail(
    post_id: int,
    request: Request,
    error: Optional[str] = None,
    db: aiosqlite.Connection = Depends(get_db),
):
    async with db.execute("SELECT * FROM posts WHERE id = ?", (post_id,)) as cursor:
        row = await cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    post = dict(row)

    async with db.execute(
        "SELECT * FROM comments WHERE post_id = ? ORDER BY created_at ASC", (post_id,)
    ) as cursor:
        comments = [dict(r) for r in await cursor.fetchall()]

    return templates.TemplateResponse(
        request=request,
        name="post_detail.html",
        context={"post": post, "comments": comments, "error": error},
    )


@router.get("/{post_id}/edit")
async def edit_post_form(
    post_id: int, request: Request, db: aiosqlite.Connection = Depends(get_db)
):
    async with db.execute("SELECT * FROM posts WHERE id = ?", (post_id,)) as cursor:
        row = await cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return templates.TemplateResponse(
        request=request, name="post_edit.html", context={"post": dict(row)}
    )


@router.post("/{post_id}/edit")
async def update_post(
    post_id: int,
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    author_id: str = Form(...),
    password: str = Form(...),
    image: Optional[UploadFile] = File(None),
    db: aiosqlite.Connection = Depends(get_db),
):
    async with db.execute("SELECT * FROM posts WHERE id = ?", (post_id,)) as cursor:
        row = await cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    post = dict(row)

    if password != post["author_password"]:
        return templates.TemplateResponse(
            request=request,
            name="post_edit.html",
            context={"post": post, "error": "비밀번호가 틀렸습니다."},
            status_code=422,
        )

    image_url = post["image_url"]
    if image and image.filename:
        _check_extension(image.filename)
        filename = f"{post_id}_{image.filename}"
        (UPLOAD_DIR / filename).write_bytes(await image.read())
        image_url = f"/static/uploads/{filename}"

    await db.execute(
        "UPDATE posts SET title=?, content=?, author_id=?, image_url=? WHERE id=?",
        (title, content, author_id, image_url, post_id),
    )
    await db.commit()
    return RedirectResponse(url=f"/posts/{post_id}", status_code=303)


@router.post("/{post_id}/delete")
async def delete_post(
    post_id: int,
    password: str = Form(...),
    db: aiosqlite.Connection = Depends(get_db),
):
    async with db.execute(
        "SELECT author_password FROM posts WHERE id = ?", (post_id,)
    ) as cursor:
        row = await cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

    if password != dict(row)["author_password"]:
        return RedirectResponse(
            url=f"/posts/{post_id}?error=wrong_password", status_code=303
        )

    await db.execute("DELETE FROM comments WHERE post_id = ?", (post_id,))
    await db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    await db.commit()
    return RedirectResponse(url="/posts", status_code=303)


@router.post("")
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    author_id: str = Form(...),
    # 실무에서는 bcrypt 등으로 해시 처리 후 저장 필요
    author_password: str = Form(...),
    image: Optional[UploadFile] = File(None),
    db: aiosqlite.Connection = Depends(get_db),
):
    async with db.execute(
        "INSERT INTO posts (title, content, author_id, author_password) VALUES (?, ?, ?, ?)",
        (title, content, author_id, author_password),
    ) as cursor:
        post_id = cursor.lastrowid
    await db.commit()

    if image and image.filename:
        _check_extension(image.filename)
        filename = f"{post_id}_{image.filename}"
        (UPLOAD_DIR / filename).write_bytes(await image.read())
        await db.execute(
            "UPDATE posts SET image_url = ? WHERE id = ?",
            (f"/static/uploads/{filename}", post_id),
        )
        await db.commit()

    return RedirectResponse(url=f"/posts/{post_id}", status_code=303)
