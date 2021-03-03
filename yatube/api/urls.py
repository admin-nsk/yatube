from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostList, PostDetail, CommentList, CommentDetail, FollowAPI, GroupAPI
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register('api/v1/posts', PostList,  basename='PostList')
router.register('api/v1/posts/(?P<post_id>[0-9])', PostDetail, basename='PostDetail')
# router.register('api/v1/follow', FollowAPI,  basename='FollowApi')

urlpatterns = [
    path('api/v1/posts/<int:post_id>/comments/', CommentList.as_view(
        actions={
            'get': 'list',
            'post': 'create',
        })),
    path('api/v1/posts/<int:post_id>/comments/<int:comment_id>/', CommentDetail.as_view(
        actions={
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        })),
    path('api/v1/follow/', FollowAPI.as_view(),  name='FollowApi'),
    path('api/v1/group/', GroupAPI.as_view(),  name='GroupApi'),
    path('', include(router.urls)),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

