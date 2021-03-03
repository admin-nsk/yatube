from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status, generics
from posts.models import Post, Comments, Follow
from group.models import Group
from .serializers import PostSerializer, CommentSerializer, FollowSerializer, GroupSerializer
from .filters import PostFilters
from .permission import IsAuthorOrReadOnlyPermission


class PostList(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnlyPermission,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnlyPermission,)


class CommentList(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnlyPermission,)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=serializer.data['post_id'])
        serializer.save(author=self.request.user, post=post)

    def list(self, request, post_id):
        comments = Comments.objects.filter(post=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def create(self, request, post_id):
        serializer = CommentSerializer(data=request.data)
        post = get_object_or_404(Post, id=post_id)
        if serializer.is_valid():
            serializer.save(author=self.request.user, post=post)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnlyPermission,)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=serializer.data['post_id'])
        serializer.save(author=self.request.user, post=post)

    def retrieve(self, request, *args, **kwargs):
        comment = get_object_or_404(self.queryset, id=kwargs['comment_id'] or None)
        serializer = self.serializer_class(comment)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        comment = get_object_or_404(self.queryset, id=kwargs['comment_id'] or None)
        if request.user == comment.author:
            serializer = self.serializer_class(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        comment = get_object_or_404(self.queryset, id=kwargs['comment_id'] or None)
        if request.user == comment.author:
            serializer = self.serializer_class(comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        comment = get_object_or_404(self.queryset, id=kwargs['comment_id'])
        if request.user == comment.author:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class FollowAPI(generics.ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GroupAPI(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
