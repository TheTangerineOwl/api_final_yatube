"""Эндпоинты API."""
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import GroupViewSet, FollowViewSet, PostViewSet, CommentViewSet

# Роутер, регистрирующий все необходимые эндпоинты для доступных типов
# запросов указанных ViewSet'ов.
router = DefaultRouter()
router.register(r'follow', FollowViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'posts', PostViewSet)

# Вложенный роутер, регистрирующий эндпоинты для модели комментария,
# зависящей от поста.
posts_router = routers.NestedDefaultRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', CommentViewSet, basename='post-comments')

urlpatterns = [
    path('v1/', include(posts_router.urls)),
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
