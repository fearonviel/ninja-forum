from handlers.base import BaseHandler
from google.appengine.api import mail


class SendMailWorker(BaseHandler):
    def post(self):

        email = self.request.get("email")
        topic_title = self.request.get("topic_title")
        topic_id = self.request.get("topic_id")

        mail.send_mail(sender="admin@ninjaforum.com", to=email, subject="New comment",
                       body=""""Tvoja tema {0} ima nov komentar.
<a href="http://ninjaforum.com/topic-details/{1}">{0}</a>""".format(topic_title, topic_id))
