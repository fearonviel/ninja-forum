#!/usr/bin/env python
import webapp2
from handlers.base import MainHandler, CookieHandler
from handlers.topics import TopicAddHandler, TopicHandler


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set-cookie', CookieHandler),
    webapp2.Route('/topic/add', TopicAddHandler, name="topic-add"),
    webapp2.Route('/topic/<topic_id:\d+>', TopicHandler, name="topic-details"),
], debug=True)
