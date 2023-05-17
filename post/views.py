from typing import Type, Optional

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from post import services
from post.models import Post, Commentary
from post.serializers import (
    PostSerializer,
    CommentarySerializer,
    PostListSerializer,
    LikePostSerializer,
    PostDetailSerializer,
    CommentaryRemoveSerializer,
)


class PostViewSet(ModelViewSet):
    """Post CRUD endpoints"""

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "list":
            return PostListSerializer

        if self.action == "retrieve":
            return PostDetailSerializer

        return super().get_serializer_class()

    @action(
        methods=["POST"],
        detail=True,
        url_path="like",
        serializer_class=LikePostSerializer,
    )
    def like(self, request: Request, pk: Optional[int] = None) -> Response:
        """Likes `obj`."""

        obj = self.get_object()
        services.add_like(obj, request.user)
        return Response("You like this post", status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=True,
        url_path="unlike",
        serializer_class=LikePostSerializer,
    )
    def unlike(self, request: Request, pk: Optional[int] = None) -> Response:
        """Dislikes `obj`."""

        obj = self.get_object()
        services.remove_like(obj, request.user)
        return Response("You don't like this post", status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=True,
        url_path="comment",
        serializer_class=CommentarySerializer,
    )
    def leave_comment(
        self, request: Request, pk: Optional[int] = None
    ) -> Response:
        """Creates comment"""

        obj = self.get_object()
        commentary = request.data.get("commentary")
        comm = Commentary.objects.create(commentary=commentary, post_id=obj.id)
        serializer = self.get_serializer(comm, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=True,
        url_path="remove",
        serializer_class=CommentaryRemoveSerializer,
    )
    def remove_all_comments(
        self, request: Request, pk: Optional[int] = None
    ) -> Response:
        """Deletes all commentaries"""

        commentaries = self.get_object().commentaries.all()
        if len(commentaries) > 0:
            return Response(
                "All commentaries deleted", status=status.HTTP_200_OK
            )

        return Response("You have no comments", status=status.HTTP_200_OK)


class CommentaryViewSet(ModelViewSet):
    """Commentary CRUD endpoints"""

    queryset = Commentary.objects.all()
    serializer_class = CommentarySerializer
