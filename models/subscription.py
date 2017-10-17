from google.appengine.ext import ndb


class Subscription(ndb.Model):
    email = ndb.StringProperty()
    topic_id = ndb.IntegerProperty()
