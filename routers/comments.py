from fastapi import APIRouter
router = APIRouter(tags=["comments"])

# TODO: 댓글 라우터를 구현하세요.
#
# 구현할 엔드포인트:
# POST /posts/{post_id}/comments  → 댓글 작성
# POST /comments/{comment_id}/delete → 댓글 삭제 (비밀번호 확인)
#
# 참고: posts.py의 create_post, delete_post 패턴과 동일한 방식으로 구현하면 됩니다.
