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
│   ├── comments.py   ← 구현해야할 파일
│   └── reset.py
├── static/
│   └── uploads/
└── templates/
    ├── list.html
    ├── post_detail.html
    ├── post_create.html
    └── post_edit.html
```

## DB 스키마

### posts

| 컬럼 | 타입 | 비고 |
|---|---|---|
| id | INTEGER PK AUTOINCREMENT | |
| title | TEXT NOT NULL | |
| content | TEXT NOT NULL | |
| author_id | TEXT NOT NULL | |
| author_password | TEXT NOT NULL | |
| image_url | TEXT | nullable |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

### comments

**여러분이 직접 설계해야 합니다.** `database.py`의 `init_db()` 안에 CREATE TABLE 구문을 추가하세요.

반드시 포함해야 할 컬럼:

| 컬럼 | 타입 | 비고 |
|---|---|---|
| id | INTEGER PK AUTOINCREMENT | |
| post_id | INTEGER NOT NULL | FK → posts.id |
| content | TEXT NOT NULL | |
| author_id | TEXT NOT NULL | |
| author_password | TEXT NOT NULL | |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

## 코드 컨벤션

- DB 접근은 `database.py`의 `get_db()`로만
- 라우터에 DB 연결 코드 직접 작성 금지
- 없는 리소스 접근 시 HTTPException 404 반환
- 이미지 저장 경로: `static/uploads/{post_id}_{filename}`
- 허용 이미지 확장자: jpg, jpeg, png, gif

## 건드리면 안 되는 파일

- `main.py`
- `database.py` — comments 테이블 추가만 허용
- `models.py`
- `routers/posts.py`
- `routers/reset.py`
- `templates/list.html`
- `templates/post_create.html`
- `templates/post_edit.html`

## 구현해야 할 것

1. **`database.py`** — `init_db()` 안에 comments 테이블 CREATE TABLE 구문 추가
2. **`routers/comments.py`** — 두 엔드포인트 구현
   - `POST /posts/{post_id}/comments` : 댓글 작성
   - `POST /comments/{comment_id}/delete` : 댓글 삭제 (비밀번호 확인)
3. **`templates/post_detail.html`** — 댓글 목록 + 댓글 작성 폼 HTML 구현

## 실행

```bash
pip install -r requirements.txt
uvicorn main:app --reload
# http://localhost:8000/posts
```
