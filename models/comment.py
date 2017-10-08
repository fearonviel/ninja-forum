from google.appengine.ext import ndb
from google.appengine.api import users, mail, taskqueue

from models.topic import Topic


class Comment(ndb.Model):
    user_email = ndb.StringProperty()
    content = ndb.TextProperty()
    topic_id = ndb.IntegerProperty()
    topic_title = ndb.StringProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    updated_at = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

    @staticmethod
    def create_comment(topic_id, content):
        user = users.get_current_user()
        topic = Topic.get_by_id(int(topic_id))

        new_comment = Comment(content=content, user_email=user.email(), topic_id=topic.key.id(),
                              topic_title=topic.title)
        new_comment.put()

        params = {"email": topic.user_email, "topic_title": topic.title, "topic_id": topic.key.id()}

        taskqueue.add(url="/task/email-topic-author", params=params)



#""" dovolijo, da se v stringu uporabijo nove vrstice in razmaki

#comment = Comment.create_comment() - na tak nacin se klice funkcija ki je znotraj class, Comment damo brez oklepajev.

