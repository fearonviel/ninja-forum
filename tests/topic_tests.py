import os
import unittest
import webapp2
import webtest

from google.appengine.api import memcache
from google.appengine.ext import testbed

from handlers.topics import TopicAddHandler, TopicHandler, DeleteTopicHandler
from handlers.base import MainHandler

from models.topic import Topic


class TopicTests(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication(
            [
                webapp2.Route('/topic/add', TopicAddHandler, name="topic-add"),
                webapp2.Route('/topic/<topic_id:\d+>/delete', DeleteTopicHandler),
                webapp2.Route('/topic/<topic_id:\d+>', TopicHandler, name="topic-details"),
                webapp2.Route('/', MainHandler, name="main-page"),
            ])

        self.testapp = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        """ Uncomment the stubs that you need to run tests. """
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # self.testbed.init_mail_stub()
        # self.testbed.init_taskqueue_stub()
        self.testbed.init_user_stub()
        # ...

        """ Uncomment if you need user (Google Login) and if this user needs to be admin. """
        os.environ['USER_EMAIL'] = 'some.user@example.com'
        # os.environ['USER_IS_ADMIN'] = '1'

    def tearDown(self):
        self.testbed.deactivate()


    def test_add_topic_handler(self):
        response = self.testapp.get('/topic/add')
        self.assertEqual(response.status_int, 200)

        memcache.add(key='abc123', value=True)
        params = {
            "csrf_token": "abc123",
            "title": "Nova tema",
            "content": "Neka vsebina teme."
        }

        response = self.testapp.post('/topic/add', params)
        self.assertEqual(response.status_int, 302)   #koda za preusmeritev je 302

        topic = Topic.query().get()
        self.assertEqual("Nova tema", topic.title)
        self.assertTrue("Neka vsebina teme.", topic.content)

    def test_topic_handler(self):
        topic = Topic(title="Test title", content="Test content", user_email="some.user@example.com")
        topic.put()

        response = self.testapp.get('/topic/{}'.format(topic.key.id()))
        self.assertEqual(response.status_int, 200)

    def test_delete_topic_handler(self):
        memcache.add(key='abc123', value=True)
        params = {"csrf_token": "abc123"}

        topic = Topic(title="Test title", content="Test content", user_email="some.user@example.com")
        topic.put()

        topic_exists = Topic.query().get()
        self.assertTrue(topic_exists)

        response = self.testapp.post('/topic/{}/delete'.format(topic.key.id()), params)
        self.assertEqual(response.status_int, 302)

        topic_deleted = Topic.query().get()
        self.assertEqual(topic_deleted.deleted, True)
