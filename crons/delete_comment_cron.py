from datetime import datetime, timedelta
from handlers.base import BaseHandler
from models.comment import Comment


class DeleteCommentsCron(BaseHandler):
    def get(self):
        month_ago = datetime.now() - timedelta(days=30)
        deleted_comments = Comment.query(Comment.deleted == True, Comment.updated_at <= month_ago).fetch()

        for comment in deleted_comments:
            comment.key.delete()