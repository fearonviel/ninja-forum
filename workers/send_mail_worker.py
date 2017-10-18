from handlers.base import BaseHandler
from google.appengine.api import mail
from models.subscription import Subscription
from models.topic import Topic


class SendMailCommentWorker(BaseHandler):
    def post(self):

        author_email = self.request.get("author_email")
        topic_title = self.request.get("topic_title")
        topic_id = self.request.get("topic_id")
        topic = Topic.get_by_id(int(topic_id))

        mail.send_mail(sender="staramarsa@gmail.com", to=author_email, subject="New comment",
                       body="""Tvoja tema {0} ima nov komentar.
<a href="http://ninjatechforum.appspot.com/topic/{1}">{0}</a>""".format(topic_title, topic_id))

        subscriptions = Subscription.query(Subscription.topic_id == topic.key.id()).fetch()

        for subscription in subscriptions:
            mail.send_mail(sender="staramarsa@gmail.com", to=subscription.email, subject="New comment",
                           body="""Tema {0} ima nov komentar.
<a href="http://ninjatechforum.appspot.com/topic/{1}">{0}</a>""".format(topic_title, topic_id))


