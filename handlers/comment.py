import cgi
from google.appengine.api import users
from handlers.base import BaseHandler
from models.comment import Comment
from models.topic import Topic
from utils.decorators import validate_csrf


class CommentHandler(BaseHandler):
    @validate_csrf
    def post(self, topic_id):

        content = cgi.escape(self.request.get("content"))
        topic = Topic.get_by_id(int(topic_id))

        Comment.create_comment(topic_id, content)

        return self.redirect_to("topic-details", topic_id=topic.key.id())


class UserCommentsHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()

        comments = Comment.query(Comment.user_email == user.email(), Comment.deleted == False,).order(-Comment.created_at).fetch()
        params = {"comments": comments}

        return self.render_template("user_comments.html", params=params)


class DeleteCommentHandler(BaseHandler):
    @validate_csrf
    def post(self, comment_id):
        user = users.get_current_user()
        comment = Comment.get_by_id(int(comment_id))

        if users.is_current_user_admin() or user.email() == comment.user_email:
            Comment.delete(comment)

        return self.redirect_to("main-page")
