from django.core import validators
from django.db import models
from django.contrib.auth import get_user_model
from group.models import Group

User = get_user_model()


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name='posts', blank=True)
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True,
        verbose_name='Изображение',
        validators=[validators.validate_image_file_extension],
        error_messages={'invalid_extension': 'Этот формат файлов не поддерживается'})

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pub_date']


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField("date published", auto_now_add=True)
