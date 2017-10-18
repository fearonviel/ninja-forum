from datetime import datetime, timedelta
from google.appengine.api import mail
from handlers.base import BaseHandler
from models.forum_subscription import ForumSubscription
from models.topic import Topic


class SendMailForumSubscribersCron(BaseHandler):
    def get(self):
        day_ago = datetime.now() - timedelta(days=1)
        emails = ForumSubscription.query().fetch()

        topics = Topic.query(Topic.deleted == False, Topic.created_at <= day_ago).fetch()

        for email in emails:
            mail.send_mail(sender="staramarsa@gmail.com", to=email.email, subject="New topics",
                           body="""Here are some new topics since the last 24h:
                           for topic in topics:
                               topic.title
                            <a href="http://ninjatechforum.appspot.">Read more</a>""")
