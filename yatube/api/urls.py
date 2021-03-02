from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostList, PostDetail
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register('api/v1/posts', PostList,  basename='PostList')
router.register('api/v1/posts/(?P<id>[0-9])', PostDetail, basename='PostDetail')

urlpatterns = [
    # path('api/v1/api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
