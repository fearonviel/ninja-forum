import cgi
from google.appengine.api import users
from handlers.base import BaseHandler
from models.topic import Topic
from models.comment import Comment
from utils.decorators import validate_csrf


class TopicAddHandler(BaseHandler):
    def get(self):
        return self.render_template_with_csrf("topic_add.html")

    @validate_csrf
    def post(self):
        user = users.get_current_user()

        title = cgi.escape(self.request.get("title"))
        text = cgi.escape(self.request.get("text"))

        new_topic = Topic(title=title, content=text, user_email=user.email())
        new_topic.put()

        return self.redirect_to("topic-details", topic_id=new_topic.key.id())


class TopicHandler(BaseHandler):
    def get(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        comments = Comment.query(Comment.topic_id == topic.key.id(), Comment.deleted == False).order(-Comment.created_at).fetch()

        params = {"topic": topic, "comments": comments}

        return self.render_template_with_csrf("topic.html", params=params)


class DeleteTopicHandler(BaseHandler):
    @validate_csrf
    def post(self, topic_id):
        user = users.get_current_user()
        topic = Topic.get_by_id(int(topic_id))
        if users.is_current_user_admin() or user.email() == topic.user_email:
            Topic.delete(topic)
        return self.redirect_to("main-page")
