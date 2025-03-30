from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import (ModelViewSet,
                                     ReadOnlyModelViewSet,
                                     GenericViewSet)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.mixins import CreateModelMixin, ListModelMixin

from posts.models import Post, Group, Comment, Follow
from .permissions import AuthorOrReadOnly
from .serializers import (PostSerializer, GroupListSerializer,
                          GroupDetailSerializer, CommentSerializer,
                          FollowSerializer)


class FollowViewSet(CreateModelMixin, ListModelMixin,
                    GenericViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostViewSet(ModelViewSet):
    """Представление поста."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorOrReadOnly, )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Создание нового поста при POST-запросе."""
        serializer.save(author=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    """Представление группы постов (только для чтения)."""

    queryset = Group.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return GroupListSerializer
        return GroupDetailSerializer


class CommentViewSet(ModelViewSet):
    """Представление комментария к посту."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly, )

    def get_queryset(self):
        """Получения списка комментариев к заданному посту (GET-запрос)."""
        post_id = self.kwargs.get('post_pk')
        return Comment.objects.filter(post=post_id)

    def perform_create(self, serializer):
        """Создание комментария к заданному посту при POST-запросе."""
        post_id = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)
