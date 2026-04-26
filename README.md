# Simple Board Project

FastAPI + SQLite 기반 게시판 실습 프로젝트입니다.
게시글 CRUD는 완성되어 있으며, **댓글 기능을 직접 구현**하는 것이 목표입니다.

---

## 환경 설정 및 실행

### 1. 가상환경 생성 및 활성화

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 서버 실행

```bash
uvicorn main:app --reload
```

### 4. 브라우저 접속

```
http://localhost:8000/posts
```

---

## 구현해야 할 기능

아래 세 파일을 수정하여 댓글 기능을 완성하세요.

### 1. `database.py`
- `init_db()` 함수 안에 `comments` 테이블 CREATE TABLE 구문 추가

반드시 포함해야 할 컬럼: `id`, `post_id`, `content`, `author_id`, `author_password`, `created_at`

### 2. `routers/comments.py`
- `POST /posts/{post_id}/comments` — 댓글 작성
- `POST /comments/{comment_id}/delete` — 댓글 삭제 (비밀번호 확인)

`routers/posts.py`의 `create_post`, `delete_post` 패턴을 참고하세요.

### 3. `templates/post_detail.html`
- 댓글 목록 출력 (라우터에서 `comments` 리스트가 전달됨)
- 댓글 작성 폼 (`action`: `POST /posts/{{ post.id }}/comments`, 필드: `content`, `author_id`, `author_password`)

---

## 건드리면 안 되는 파일

| 파일 | 이유 |
|---|---|
| `main.py` | 앱 진입점, 라우터 등록 완료 |
| `routers/posts.py` | 게시글 기능 완성본 (참고용) |
| `routers/reset.py` | DB 초기화 유틸리티 |
| `models.py` | Pydantic 모델 (댓글 모델 불필요) |
| `templates/list.html` | 게시글 목록 페이지 |
| `templates/post_create.html` | 게시글 작성 페이지 |
| `templates/post_edit.html` | 게시글 수정 페이지 |

---

## 브랜치 안내

| 브랜치 | 설명 |
|---|---|
| `main` | 실습용 코드 (현재 브랜치, 댓글 미구현) |
| `solution` | 완성본 (참고용) |

---

## API 문서

서버 실행 후 아래에서 Swagger UI를 확인할 수 있습니다.

```
http://localhost:8000/docs
```

---

## 기타

- DB 초기화: `POST /reset` (서버 실행 중 호출)
- 이미지 업로드: 게시글 작성/수정 시 jpg, jpeg, png, gif 허용
- 업로드된 이미지는 `static/uploads/`에 저장됩니다.
