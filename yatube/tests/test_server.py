from django.test import TestCase, Client

from django.urls import reverse

from posts.models import Post, User


class TestServer(TestCase):

    def setUp(self):
        self.client = Client()

    def test_404(self):
        response = self.client.get('/last/')
        self.assertEqual(response.status_code, 404)
