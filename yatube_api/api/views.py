from django.shortcuts import get_object_or_404
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import bad_request

from posts.models import Post, Group, Comment, Follow, User
from .permissions import AuthorOrReadOnly
from .serializers import (PostSerializer, GroupListSerializer,
                          GroupDetailSerializer, CommentSerializer,
                          FollowSerializer)


class FollowViewSet(ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        request_following = serializer.instance.following
        following_instance = User.objects.filter(
            username=request_following).first()
        if following_instance is None:
            return bad_request(self.request,
                               "Такого пользователя не существует!")
        if self.request.user == serializer.instance.following:
            return bad_request(self.request,
                               "Нельзя подписаться на самого себя!")
        serializer.save(user=self.request.user)


class PostViewSet(ModelViewSet):
    """Представление поста."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorOrReadOnly, )
    pagination_class = (LimitOffsetPagination, )

    def perform_create(self, serializer):
        """Создание нового поста при POST-запросе."""
        serializer.save(author=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    """Представление группы постов (только для чтения)."""

    queryset = Group.objects.all()
    # serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_serializer_class(self):
        if self.action == 'list':
            return GroupListSerializer
        return GroupDetailSerializer


class CommentViewSet(ModelViewSet):
    """Представление комментария к посту."""

    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly, )

    def get_queryset(self):
        """Получения списка комментариев к заданному посту (GET-запрос)."""
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post=post_id)

    def perform_create(self, serializer):
        """Создание комментария к заданному посту при POST-запросе."""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)
