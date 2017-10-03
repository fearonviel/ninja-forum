import cgi
from google.appengine.api import users
from handlers.base import BaseHandler
from models.comment import Comment
from models.topic import Topic
from utils.decorators import validate_csrf


class CommentHandler(BaseHandler):
    @validate_csrf
    def post(self, topic_id):
        user = users.get_current_user()
        topic = Topic.get_by_id(int(topic_id))

        content = cgi.escape(self.request.get("content"))

        new_comment = Comment(content=content, user_email=user.email(), topic_id=topic.key.id(), topic_title=topic.title)
        new_comment.put()

        return self.redirect_to("topic-details", topic_id=topic.key.id())


