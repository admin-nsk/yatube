from rest_framework import serializers

from posts.models import Post, Comments, Follow
from group.models import Group


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comments


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    following = serializers.CharField(source='author.username')

    class Meta:
        model = Follow
        fields = ('user', 'following')


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['title']
