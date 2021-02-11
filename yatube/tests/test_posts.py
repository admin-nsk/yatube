from django.test import TestCase, Client

from django.urls import reverse
from django.core.cache import cache
from posts.models import Post, User


class TestPosts(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_username = 'testuser'
        self.test_email = 'testuser@mail.com'
        self.test_password = '12345'
        self.user = User.objects.create_user(
            username=self.test_username,
            email=self.test_email,
            password=self.test_password)
        self.guest = User.objects.create_user(username='guest', email='guest@mail.com', password='54321')
        self.post = Post.objects.create(
            text='Давно выяснено, что при оценке дизайна и композиции читаемый текст мешает сосредоточиться. '
                 'Lorem Ipsum используют потому, что тот обеспечивает более или менее',
            author=self.user,
            image='test-img.jpg'
            )
        self.post_id = self.post.id

    def test_profile(self):
        self.client.login(username=self.test_username, password=self.test_password)
        response = self.client.get(f'/{self.user.username}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page"]), 1)
        self.assertIsInstance(response.context["author"], User)
        self.assertEqual(response.context["author"].username, self.user.username)
        text_img = "<img "
        self.assertContains(response, text_img, status_code=200)

    def test_create_post(self):
        if self.client.login(username=self.test_username, password=self.test_password, follow=True):
            with open('media/test-img.jpg', 'rb') as img:
                response = self.client.post('/new/', {'text': 'test post for testuser', 'image': img}, follow=True)
            self.assertEqual(response.status_code, 200)

    def test_fail_create_post(self):
        self.client.login(username='test', password='12345', follow=True)
        response = self.client.post('/new/', {'text': 'test post for testuser'}, follow=True)
        self.assertRedirects(response, '/auth/login/?next=/new/', status_code=302, target_status_code=200)

    def test_newpost_on_index(self):
        cache.clear()
        posts = self.user.posts.all()
        for post in posts:
            for url in (
                reverse('index'),
                reverse('profile', kwargs={'username': self.user.username}),
                reverse('post', kwargs={'username': self.user.username, 'post_id': post.id})
            ):
                response = self.client.get(url)
                text_img = "<img "
                self.assertContains(response, text_img, status_code=200)
                self.assertContains(response, post.text)

    def test_edit_post(self):
        posts = self.user.posts.all()
        if self.client.login(username=self.test_username, password=self.test_password, follow=True):
            for post in posts:
                response = self.client.post(
                    reverse('post_edit', kwargs=
                            {'username': self.user.username,
                             'post_id': post.id,
                             }), {'text': 'Modify text in the post'}, follow=True)
                self.assertEqual(response.status_code, 200)
        cache.clear()
        posts_new = self.user.posts.all()
        for post in posts_new:
            for url in (
                reverse('index'),
                reverse('profile', kwargs={'username': self.user.username}),
                reverse('post', kwargs={'username': self.user.username, 'post_id': post.id})
            ):
                response = self.client.get(url)
                self.assertContains(response, post.text)

    def test_post_have_img(self):
        post = self.user.posts.first()
        response = self.client.get(reverse('post', kwargs={'username': self.user.username, 'post_id': self.post_id}))
        text_img = "<img "
        self.assertContains(response, text_img, status_code=200)

    def test_load_no_image(self):
        post = self.user.posts.first()
        if self.client.login(username=self.test_username, password=self.test_password, follow=True):
            with open('media/test-load.js', 'rb') as img:
                response = self.client.post(
                    reverse('post_edit', kwargs=
                    {'username': self.user.username,
                     'post_id': post.id,
                     }), {'text': 'Modify text in the post', 'image': img}, follow=True)
            self.assertContains(response, 'errorlist', status_code=200)

    def test_cache_index_page(self):
        if self.client.login(username=self.test_username, password=self.test_password, follow=True):
            self.client.get('/')
            response_post = self.client.post('/new/', {'text': 'test cache'}, follow=True)
            self.assertEqual(response_post.status_code, 200)
            response = self.client.get('/')
            self.assertNotContains(response, 'test cache')
            cache.clear()
            response = self.client.get('/')
            self.assertContains(response, 'test cache')