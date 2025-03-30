"""Сериализаторы приложения API."""
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Post, Follow, Group, User


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор сообщества."""

    class Meta:
        """Метаданные сериализатора."""

        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор подписки."""

    user = serializers.ReadOnlyField(source='user.username')
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        error_messages={
            'does_not_exist': "Объект с username={following} не существует.",
            'invalid': 'Неверное значение для поля following.'
        }
    )

    class Meta:
        """Метаданные сериализатора."""

        fields = '__all__'
        model = Follow

    def validate(self, data):
        """Валидация данных подписки."""
        user = self.context['request'].user
        following = data['following']
        if user == following:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя!")
        if Follow.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError(
                "Вы уже подписаны на этого пользователя.")
        return data


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор поста."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        """Метаданные сериализатора."""

        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментария к записи."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """Метаданные комментария."""

        fields = '__all__'
        model = Comment
