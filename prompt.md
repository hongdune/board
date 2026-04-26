# 사용한 프롬프트

```
CLAUDE.md 읽어줘.

읽었으면 아래 순서대로 진행해:
1. requirements.txt 생성
2. 폴더 구조 및 빈 파일 생성 (routers/, static/uploads/, templates/)
3. database.py 작성 — DB 연결, posts/comments 테이블 초기화
4. models.py 작성 — Post, Comment Pydantic 모델
5. main.py 작성 — 앱 초기화, 라우터 등록, static/templates 마운트

각 파일 작성 후 다음으로 넘어가기 전에 확인 요청해줘.
```

```
posts 라우터부터 만들어줘.

구현할 엔드포인트:
- GET  /posts              → list.html 렌더링
- GET  /posts/{post_id}    → post_detail.html 렌더링
- POST /posts              → 글 작성, 이미지 업로드 처리 후 상세 페이지로 redirect

템플릿은 라우터 작성 후 같이 만들어줘.
list.html → post_detail.html → post_create.html 순서로.
```

```
comments 라우터 만들어줘.

구현할 엔드포인트:
- POST /posts/{post_id}/comments   → 댓글 작성 후 상세 페이지로 redirect
- DELETE /comments/{comment_id}    → 댓글 삭제

post_detail.html에 댓글 목록과 작성 폼도 추가해줘.
```

```
아래 오류가 발생했어.

TypeError: cannot use 'tuple' as a dict key (unhashable type: 'dict')
routers/posts.py line 31, list_posts 함수에서
templates.TemplateResponse("list.html", ...) 호출 시 발생

원인 파악하고 수정해줘.
list.html이 없으면 같이 만들어줘.

표시할 데이터:
- 글 목록 (title, author_nickname, created_at)
- 각 글 클릭 시 /posts/{post_id} 로 이동
- 새 글 작성 버튼 → /posts/new 로 이동

스타일은 외부 프레임워크 없이 <style> 태그로, 깔끔하게.
이후 post_create.html, post_detail.html도 같은 스타일 기준으로 만들 거야.
```

```
게시판 CRUD 완성을 위해 아래 기능을 추가해줘.

1. 글 수정
   - GET  /posts/{post_id}/edit  → 수정 폼 페이지 (post_edit.html 새로 생성)
   - POST /posts/{post_id}/edit  → 수정 처리 후 상세 페이지로 redirect
   - 이미지도 변경 가능해야 함 (새 이미지 업로드 시 기존 파일 덮어쓰기)

2. 글 삭제
   - POST /posts/{post_id}/delete → 삭제 처리 후 목록으로 redirect
   - (DELETE 메서드 대신 POST 쓰는 이유: HTML form은 GET/POST만 지원)

3. 예외/엣지케이스 처리
   - 존재하지 않는 post_id 접근 시 404 반환 (이미 돼있으면 확인만)
   - list.html: 글이 0개일 때 "아직 글이 없습니다" 안내 문구
   - post_detail.html: image_url이 null이면 이미지 영역 표시 안 함
```

```
DC 인사이드처럼 회원가입 없이 글 작성 시 ID/PW를 입력하고
수정/삭제 시 해당 PW를 확인하는 방식으로 인증을 추가해줘.

변경사항:
1. database.py
   - posts 테이블에 author_id(TEXT), author_password(TEXT) 컬럼 추가
   - 기존 board.db 파일 있으면 삭제하고 재생성

2. post_create.html + POST /posts
   - 작성 폼에 ID, PW 입력 필드 추가
   - DB 저장 시 평문으로 저장 (주석으로 실무에서는 해시 처리 필요하다고 명시)

3. post_edit.html + POST /posts/{post_id}/edit
   - 수정 폼 상단에 PW 확인 필드 추가
   - 입력한 PW와 DB 저장값 불일치 시 "비밀번호가 틀렸습니다" 메시지 표시
   - 일치 시에만 수정 처리

4. POST /posts/{post_id}/delete
   - 삭제 요청에 PW 포함
   - 불일치 시 상세 페이지로 돌아가며 에러 메시지 표시
   - 일치 시 삭제 후 목록으로 redirect
```

```
현재 닉네임과 아이디의 역할이 중복되어 둘 다 아이디로 통일하고 동일한 기능을 댓글에도 적용해야해.
```