from django.urls import path, include
from rest_framework import routers

from post.views import PostViewSet, CommentaryViewSet

router = routers.DefaultRouter()
router.register("posts", PostViewSet)
router.register("commentaries", CommentaryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "posts"
