from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from posts.models import Post
from .serializers import PostSerializer
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