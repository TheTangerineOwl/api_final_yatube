"""Модели для сущностей блога."""
from django.contrib.auth import get_user_model
from django.db import models

# Получение встроенной модели пользователя.
User = get_user_model()


class Group(models.Model):
    """Сообщество для постов."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        """Группа постов представляется своим названием."""
        return self.title


class Follow(models.Model):
    """Подписка пользователя на другого."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE, related_name="follower"
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE, related_name="follow"
    )

    def __str__(self):
        """Подписка представляется именем пользователя."""
        return self.following

    class Meta:
        """Метаданные модели подписки."""

        unique_together = ('user', 'following')


class Post(models.Model):
    """Модель поста в блоге."""

    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        """Пост представляется своим текстом."""
        return self.text


class Comment(models.Model):
    """Модель комментария к посту."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
