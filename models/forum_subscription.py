from google.appengine.ext import ndb


class ForumSubscription(ndb.Model):
    email = ndb.StringProperty()
