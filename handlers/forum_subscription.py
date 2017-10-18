from google.appengine.api import users

from handlers.base import BaseHandler
from models.forum_subscription import ForumSubscription
from utils.decorators import validate_csrf


class ForumSubscriptionHandler(BaseHandler):
    @validate_csrf
    def post(self):
        user = users.get_current_user()

        new_forum_subscription = ForumSubscription(email=user.email())
        new_forum_subscription.put()

        return self.redirect_to("main-page")
