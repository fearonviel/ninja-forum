import os
import unittest
import webapp2
import webtest

from google.appengine.api import memcache
from google.appengine.ext import testbed

from handlers.comment import CommentHandler, DeleteCommentHandler, UserCommentsHandler
from handlers.topics import TopicHandler
from handlers.base import MainHandler

from models.topic import Topic
from models.comment import Comment


class CommentsTests(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication(
            [
                webapp2.Route('/', MainHandler, name="main-page"),
                webapp2.Route('/user-comments', UserCommentsHandler, name="user-comments"),
                webapp2.Route('/comment/<comment_id:\d+>/delete', DeleteCommentHandler),
                webapp2.Route('/topic/<topic_id:\d+>/comment/add', CommentHandler),
                webapp2.Route('/topic/<topic_id:\d+>', TopicHandler, name="topic-details"),
            ])

        self.testapp = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        """ Uncomment the stubs that you need to run tests. """
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # self.testbed.init_mail_stub()
        self.testbed.init_taskqueue_stub()
        self.testbed.init_user_stub()
        # ...

        """ Uncomment if you need user (Google Login) and if this user needs to be admin. """
        os.environ['USER_EMAIL'] = 'some.user@example.com'
        # os.environ['USER_IS_ADMIN'] = '1'

    def tearDown(self):
        self.testbed.deactivate()


    def test_add_comment_handler(self):

        memcache.add(key='abc123', value=True)

        topic = Topic(title="Test title", content="Test content", user_email="some.user@example.com")
        topic.put()

        params = {
            "csrf_token": "abc123",
            "topic_id": topic.key.id(),
            "content": "New comment."
        }

        response = self.testapp.post('/topic/{}/comment/add'.format(topic.key.id()), params)
        self.assertEqual(response.status_int, 302)

        comment = Comment.query().get()
        self.assertEqual("New comment.", comment.content)

    def test_user_comments_handler(self):
        response = self.testapp.get('/user-comments')
        self.assertEqual(response.status_int, 200)

    def test_delete_comment_handler(self):
        memcache.add(key='abc123', value=True)
        params = {"csrf_token": "abc123"}

        topic = Topic(title="Test title", content="Test content", user_email="some.user@example.com")
        topic.put()

        comment = Comment(content="New comment.", topic_id=topic.key.id(), user_email="some.user@example.com")
        comment.put()

        comment_exist = Comment.query().get()
        self.assertTrue(comment_exist)

        response = self.testapp.post('/comment/{}/delete'.format(comment.key.id()), params)
        self.assertEqual(response.status_int, 302)

        comment_deleted = Comment.query().get()
        self.assertTrue(comment_deleted.deleted)
