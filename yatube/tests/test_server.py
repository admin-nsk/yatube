from django.test import TestCase, Client
from django.urls import reverse
from posts.models import Post, User

class TestServer(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_username1 = 'testuser1'
        self.test_username2 = 'testuser2'
        self.test_email = 'testuser@mail.com'
        self.test_password = '12345'
        self.user1 = User.objects.create_user(
            username=self.test_username1,
            email=self.test_email,
            password=self.test_password)
        self.user2 = User.objects.create_user(
            username=self.test_username2,
            email=self.test_email,
            password=self.test_password)
        self.guest = User.objects.create_user(username='guest', email='guest@mail.com', password='54321')
        self.post = Post.objects.create(
            text='Тестовый пост первого пользователя',
            author=self.user1,
            image='test-img.jpg'
        )
        self.post_two = Post.objects.create(
            text='Тестовый пост второго пользователя',
            author=self.user2,
            image='test-img.jpg'
        )
        self.post_id = self.post.id

    def test_404(self):
        response = self.client.get('/last/')
        self.assertEqual(response.status_code, 404)

    def test_auth_user_subscribe(self):
        if self.client.login(username=self.test_username1, password=self.test_password, follow=True):
            response = self.client.get(f'/{self.user2.username}/')
            self.assertEqual(response.status_code, 200)
            response = self.client.post(f'/{self.user2.username}/follow/', username=self.user2.username, follow=True)
            self.assertEqual(response.status_code, 200)
            response = self.client.post(f'/{self.user2.username}/unfollow/', username=self.user2.username, follow=True)
            self.assertEqual(response.status_code, 200)

    def test_post_following_user(self):
        if self.client.login(username=self.test_username1, password=self.test_password, follow=True):
            response = self.client.get('/follow/')
            self.assertNotContains(response, 'Тестовый пост второго пользователя')
            response = self.client.post(f'/{self.user2.username}/follow/', username=self.user2.username, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Тестовый пост второго пользователя')

    def test_create_comments(self):
        self.client.login(username='test', password='12345', follow=True)
        response = self.client.post(f'/{self.user1.username}/{self.post.id}/comment', {'text': 'test comment'}, follow=True)
        self.assertNotContains(response, 'test comment')
        if self.client.login(username=self.test_username1, password=self.test_password, follow=True):
            response = self.client.post(f'/{self.user1.username}/{self.post.id}/comment', {'text': 'test comment'},
                                        follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'test comment')

