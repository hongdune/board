# Simple Board Project

FastAPI + SQLite 기반 게시판 실습 프로젝트입니다.
게시글 CRUD는 완성되어 있으며, **댓글 기능을 직접 구현**하는 것이 목표입니다.

---

## 환경 설정 및 실행

### 1. Git Clone
```bash
git clone https://github.com/hongdune/board.git
cd board
```

### 2. 가상환경 생성 및 활성화
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. 서버 실행
```bash
uvicorn main:app --reload
```

### 5. 브라우저 접속
```
http://localhost:8000/posts
```

---

## 구현해야 할 기능

아래 세 파일을 수정하여 댓글 기능을 완성하세요.
각 항목의 **입력 / 출력 / 동작**을 만족하면 됩니다.

---

### 1. `database.py`

#### 작업 위치
`init_db()` 함수 내부, posts 테이블 생성 코드 다음

#### 명세
- **목적:** comments 테이블을 SQLite DB에 생성
- **입력:** 없음 (서버 시작 시 자동 호출됨)
- **출력:** 없음 (DB에 테이블이 생성되는 부수 효과)

#### 필수 컬럼

| 컬럼명 | 타입 | 제약 | 비고 |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | 댓글 고유 ID |
| `post_id` | INTEGER | NOT NULL | 어느 게시글의 댓글인지 (posts.id 참조) |
| `content` | TEXT | NOT NULL | 댓글 내용 |
| `author_id` | TEXT | NOT NULL | 작성자 아이디 |
| `author_password` | TEXT | NOT NULL | 작성자 비밀번호 (실습용 평문 저장) |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 작성 시각 |

> 💡 posts 테이블 생성 코드를 참고하면 패턴이 동일합니다.

---

### 2. `routers/comments.py`

#### 엔드포인트 1 — 댓글 작성

**`POST /posts/{post_id}/comments`**

| 항목 | 내용 |
|---|---|
| **입력 (Path)** | `post_id: int` — 댓글이 달릴 게시글 ID |
| **입력 (Form)** | `content: str` — 댓글 내용<br>`author_id: str` — 작성자 아이디<br>`author_password: str` — 작성자 비밀번호 |
| **동작** | 1. `post_id`가 존재하는 게시글인지 확인<br>2. 없으면 404 반환<br>3. 있으면 comments 테이블에 INSERT<br>4. 게시글 상세 페이지로 redirect |
| **출력 (성공)** | `RedirectResponse` → `/posts/{post_id}` (status 303) |
| **출력 (실패)** | 게시글 없음: `HTTPException 404` |

#### 엔드포인트 2 — 댓글 삭제

**`POST /comments/{comment_id}/delete`**

| 항목 | 내용 |
|---|---|
| **입력 (Path)** | `comment_id: int` — 삭제할 댓글 ID |
| **입력 (Form)** | `password: str` — 삭제 인증용 비밀번호 |
| **동작** | 1. `comment_id`로 댓글 조회<br>2. 없으면 404 반환<br>3. 입력 비밀번호와 DB의 `author_password` 비교<br>4. 불일치 시 403 반환<br>5. 일치 시 댓글 삭제 |
| **출력 (성공)** | JSON: `{"ok": true}` |
| **출력 (실패)** | 댓글 없음: `HTTPException 404`<br>비밀번호 불일치: `JSONResponse 403` `{"detail": "비밀번호가 틀렸습니다."}` |

> 💡 `routers/posts.py`의 `create_post`, `delete_post` 패턴을 참고하세요.

---

### 3. `templates/post_detail.html`

`post_detail` 라우터에서 아래 데이터가 템플릿으로 전달됩니다.

#### 템플릿이 받는 데이터 (Context)

| 변수명 | 타입 | 설명 |
|---|---|---|
| `post` | dict | 게시글 정보 (이미 사용 중) |
| `comments` | list[dict] | 댓글 목록 (새로 추가됨) |

#### `comments` 리스트의 각 요소 구조
```python
{
    "id": int,
    "post_id": int,
    "content": str,
    "author_id": str,
    "author_password": str,    # 화면 노출 금지
    "created_at": str          # ISO 형식 문자열
}
```

#### 구현해야 할 UI 요소

**A. 댓글 목록 표시**
- **입력:** `comments` 리스트
- **출력 요구사항:**
  - 댓글이 0개일 때 "아직 댓글이 없습니다" 같은 안내
  - 각 댓글마다 표시: `content`, `author_id`, `created_at`
  - 각 댓글에 삭제 버튼 (클릭 시 비밀번호 받아 삭제 API 호출)
  - `author_password`는 절대 화면에 표시하지 말 것

**B. 댓글 작성 폼**
- **출력 요구사항 (HTML):**
  - `<form method="post" action="/posts/{{ post.id }}/comments">`
  - 필드 3개: `content` (textarea), `author_id` (input), `author_password` (input type="password")
  - 모두 `required` 속성 필요

**C. 삭제 처리 (JavaScript)**
- 삭제 버튼 클릭 → 비밀번호 입력 받기 (`prompt()` 등)
- `POST /comments/{comment_id}/delete`로 form-data 전송 (필드: `password`)
- 응답이 200이면 해당 댓글 DOM 제거
- 응답이 403/404이면 에러 메시지 표시

---

## 동작 검증 체크리스트

구현 후 아래 시나리오로 직접 테스트하세요.

```
□ 게시글 목록 → 글 하나 클릭 → 상세 페이지 진입
□ 상세 페이지 하단에 댓글 작성 폼이 보인다
□ 댓글 작성 폼에 내용 입력 후 제출 → 같은 페이지로 돌아옴
□ 작성한 댓글이 목록에 보인다
□ 삭제 버튼 클릭 → 비밀번호 입력
□ 올바른 비밀번호 입력 시 댓글이 사라진다
□ 틀린 비밀번호 입력 시 에러 메시지가 뜬다
□ 존재하지 않는 게시글에 댓글 시도 → 404
□ 다른 게시글에 가도 댓글이 게시글별로 분리된다
```

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
| `solution` | 완성본 (실습 후 비교용) |

---

## 참고 자료

- **API 문서 (Swagger):** http://localhost:8000/docs
- **DB 초기화:** `POST /reset` (서버 실행 중 호출 시 DB 리셋)
- **이미지 업로드:** jpg, jpeg, png, gif 허용 / `static/uploads/`에 저장

---

## 막혔을 때

1. 먼저 `routers/posts.py`의 비슷한 함수를 참고하세요
2. 그래도 막히면 Claude Code에 다음과 같이 물어보세요:

   ```
   CLAUDE.md를 참고해서 댓글 작성 API를 구현하려고 해.
   posts.py의 create_post와 비슷한 패턴으로 만들고 싶어.

   요구사항:
   - POST /posts/{post_id}/comments
   - Form 입력: content, author_id, author_password
   - 게시글 존재 확인 후 INSERT
   - 성공 시 /posts/{post_id}로 redirect

   구현해줘.
   ```

3. 에러가 나면 에러 메시지 전체를 Claude에게 그대로 전달하세요.

