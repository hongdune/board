# Simple Board Project (Solution)

이 저장소는 FastAPI 기반 게시판 프로젝트의 **완성본(Solution)**입니다.
학생용 과제(`main` 브랜치)의 정답 구현을 포함하고 있습니다.
단, 정답의 의미는 강사가 상정한 최종 결과물일뿐 실제 구현된 결과는 이와 동일하지 않는게 정상이며 지시한 동작만 충족하면 정답입니다.

---

## 프로젝트 개요

* 게시글 CRUD (생성 / 조회 / 수정 / 삭제)
* 댓글 기능 (작성 / 삭제)
* 이미지 업로드 지원
* SQLite 기반 비동기 데이터 처리

---

## 기술 스택

* Python
* FastAPI
* SQLite
* Jinja2
* aiosqlite

---

## 프로젝트 구조

```
.
├── main.py
├── database.py
├── models.py
├── routers/
│   ├── posts.py
│   └── comments.py
├── templates/
├── static/
│   └── uploads/
├── requirements.txt
└── README.md
```

---

## 실행 방법

### 1. 가상환경 생성 및 활성화

```
python -m venv .venv
.venv\Scripts\activate   # Windows
```

### 2. 패키지 설치

```
pip install -r requirements.txt
```

### 3. 서버 실행

```
uvicorn main:app --reload
```

### 4. 접속

```
http://localhost:8000
```

---

## 주요 기능 설명

### 게시글 (Posts)

* 게시글 생성 및 목록 조회
* 상세 조회
* 비밀번호 기반 수정 / 삭제

### 댓글 (Comments)

* 댓글 작성
* 비밀번호 기반 삭제

### 이미지 업로드

* 게시글 작성 시 이미지 URL 저장
* `static/uploads/` 경로 활용 가능

---

## 데이터베이스

* SQLite (`board.db`) 사용
* 서버 실행 시 자동으로 테이블 생성

### 테이블 구조

#### posts

* id (PK)
* title
* content
* author_id
* author_password
* image_url
* created_at

#### comments

* id (PK)
* post_id (FK)
* content
* author_id
* author_password
* created_at

---

## 브랜치 구조

* `main` → 학생용 코드 (일부 기능 미구현)
* `solution` → 현재 브랜치 (완성본)

---

## 주의사항

* 업로드 파일은 버전 관리 대상 아님
* `static/uploads/.gitkeep`은 폴더 유지를 위한 파일

---

## 개발 참고

* API 문서: `/docs` (Swagger UI)
* DB 초기화: `POST /reset`

---

## 목적

이 프로젝트는 다음을 학습하기 위한 예제입니다:

* FastAPI 라우터 구조 설계
* 비동기 DB 처리
* 템플릿 기반 웹 서비스 구현
* 간단한 인증 로직 (비밀번호 검증)

---

## 라이선스

교육 및 학습 목적의 프로젝트입니다.
