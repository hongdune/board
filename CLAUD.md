# CLAUDE.md

## 프로젝트 개요

FastAPI + SQLite 기반 게시판 웹 애플리케이션.
Jinja2 템플릿으로 서버사이드 렌더링. 별도 프론트엔드 프레임워크 없음.

## 기술 스택

- **Backend:** FastAPI, uvicorn
- **DB:** SQLite (aiosqlite)
- **Template:** Jinja2
- **기타:** python-multipart (파일 업로드)

## 프로젝트 구조

```
project/
├── main.py
├── database.py
├── models.py
├── requirements.txt
├── routers/
│   ├── posts.py
│   └── comments.py
├── static/
│   └── uploads/
└── templates/
    ├── list.html
    ├── post_detail.html
    └── post_create.html
```

## DB 스키마

### posts

| 컬럼 | 타입 | 비고 |
|---|---|---|
| id | INTEGER PK AUTOINCREMENT | |
| title | TEXT NOT NULL | |
| content | TEXT NOT NULL | |
| author_nickname | TEXT NOT NULL | |
| image_url | TEXT | nullable |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

### comments

| 컬럼 | 타입 | 비고 |
|---|---|---|
| id | INTEGER PK AUTOINCREMENT | |
| post_id | INTEGER NOT NULL | FK → posts.id |
| content | TEXT NOT NULL | |
| author_nickname | TEXT NOT NULL | |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

## 코드 컨벤션

- DB 접근은 `database.py`의 `get_db()`로만
- 라우터에 DB 연결 코드 직접 작성 금지
- 없는 리소스 접근 시 HTTPException 404 반환
- 이미지 저장 경로: `static/uploads/{post_id}_{filename}`
- 허용 이미지 확장자: jpg, jpeg, png, gif

## 실행

```bash
pip install -r requirements.txt
uvicorn main:app --reload
# http://localhost:8000/posts
```
