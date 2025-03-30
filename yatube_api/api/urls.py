from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import GroupViewSet, FollowViewSet, PostViewSet, CommentViewSet


router = DefaultRouter()
router.register('groups', GroupViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]

urlpatterns += [
    # TODO: добавить нижестоящие пути после реализации ViewSet'ов

    # path('v1/follow/', ...),    # GET POST                              LIST
    # path('v1/groups/{id}/', ...),  # GET                                DETAIL
    # path('v1/groups/', ...),  # GET!!!!!!!                                LIST
    # path('v1/posts/{post_id}/comments/{id}/', ...), # GET PUT PATCH DEL    DETAIL
    # path('v1/posts/<int:post_id>/comments/', ...), # GET POST          LIST
    # path('v1/posts/<int:id>/', ...), # GET PUT PATCH DEL               DETAIL
    # path('v1/posts/', ...), # get post                               LIST
    # path('v1/jwt/create/', ...),        auth/jwt/create
    # path('v1/jwt/refresh', ...),          auth/jwt/refresh
    # path('v1/jwt/verify', ...)
]
