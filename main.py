#!/usr/bin/env python
import webapp2
from handlers.base import MainHandler, CookieHandler
from handlers.topics import TopicAddHandler, TopicHandler, DeleteTopicHandler
from handlers.comment import CommentHandler, UserCommentsHandler
from workers.send_mail_worker import SendMailWorker
from crons.delete_topics_cron import DeleteTopicsCron


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set-cookie', CookieHandler),
    webapp2.Route('/topic/add', TopicAddHandler, name="topic-add"),
    webapp2.Route('/topic/<topic_id:\d+>', TopicHandler, name="topic-details"),
    webapp2.Route('/topic/<topic_id:\d+>/comment/add', CommentHandler),
    webapp2.Route('/topic/<topic_id:\d+>/delete', DeleteTopicHandler),
    webapp2.Route('/user-comments', UserCommentsHandler, name="user-comments"),

    webapp2.Route('/cron/delete-topics', DeleteTopicsCron),

    webapp2.Route('/task/email-topic-author', SendMailWorker),
], debug=True)
