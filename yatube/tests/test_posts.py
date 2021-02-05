from django.test import TestCase, Client

from django import forms
from django.urls import reverse

from posts.models import Post, User


class TestPosts(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='testuser@mail.com', password='12345')
        self.guest = User.objects.create_user(username='guest', email='guest@mail.com', password='54321')
        self.post = Post.objects.create(
            text='Давно выяснено, что при оценке дизайна и композиции читаемый текст мешает сосредоточиться. '
                 'Lorem Ipsum используют потому, что тот обеспечивает более или менее',
            author=self.user
        )

    def test_profile(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(f'/{self.user.username}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page"]), 1)
        self.assertIsInstance(response.context["author"], User)
        self.assertEqual(response.context["author"].username, self.user.username)

    def test_create_post(self):
        if self.client.login(username='testuser', password='12345', follow=True):
            response = self.client.post('/new/', {'text': 'test post for testuser'}, follow=True)
            self.assertEqual(response.status_code, 200)

    def test_fail_create_post(self):
        self.client.login(username='test', password='12345', follow=True)
        response = self.client.post('/auth/login/?next=/new/', {'text': 'test post for testuser'}, follow=True)

    def test_newpost_on_index(self):
        posts = self.user.posts.all()
        for post in posts:
            for url in (
                reverse('index'),
                reverse('profile', kwargs={'username': self.user.username}),
                reverse('post', kwargs={'username': self.user.username, 'post_id': post.id})
            ):
                response = self.client.get(url)
                self.assertContains(response, post.text)

    def test_edit_post(self):
        posts = self.user.posts.all()
        if self.client.login(username='testuser', password='12345', follow=True):
            for post in posts:
                response = self.client.post(
                    reverse('post_edit', kwargs=
                            {'username': self.user.username,
                             'post_id': post.id,
                             }), {'text': 'Modify text in the post'}, follow=True)
                self.assertEqual(response.status_code, 200)
        posts_new = self.user.posts.all()
        for post in posts_new:
            for url in (
                reverse('index'),
                reverse('profile', kwargs={'username': self.user.username}),
                reverse('post', kwargs={'username': self.user.username, 'post_id': post.id})
            ):
                response = self.client.get(url)
                self.assertContains(response, post.text)