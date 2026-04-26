# 별도 추가

from fastapi import APIRouter
from database import reset_db

router = APIRouter()

@router.post("/reset")
async def reset():
    await reset_db()
    return {"message": "DB reset complete"}