from handlers.base import BaseHandler
from google.appengine.api import users
from models.topic import Topic


class TopicAddHandler(BaseHandler):
    def get(self):
        return self.render_template("topic_add.html")

    def post(self):
        user = users.get_current_user()

        if not user:
            return self.write("Please login to add a new topic.")

        title = self.request.get("title")
        text = self.request.get("text")

        new_topic = Topic(title=title, content=text, user_email=user.email())
        new_topic.put()

        return self.write("Successful.")

