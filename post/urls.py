from django.urls import path, include
from rest_framework import routers

from post.views import PostViewSet, CommentaryViewSet

router = routers.DefaultRouter()
router.register("posts", PostViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
    path("commentaries/", CommentaryViewSet.as_view(), name="commentaries"),
]

app_name = "posts"
