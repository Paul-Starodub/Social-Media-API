from typing import Type, Optional

from django.db.models import QuerySet, Q
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, generics
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from post import services
from post.models import Post, Commentary
from post.permissions import IsAuthenticatedOrAnonymous
from post.serializers import (
    PostSerializer,
    CommentarySerializer,
    PostListSerializer,
    LikePostSerializer,
    CommentaryRemoveSerializer,
)
from user.models import UserFollowing


@extend_schema(
    parameters=[
        OpenApiParameter("pk", OpenApiTypes.STR, OpenApiParameter.PATH)
    ]
)
class PostViewSet(ModelViewSet):
    """Post CRUD endpoints"""

    lookup_field = "pk"
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrAnonymous,)

    def get_queryset(self) -> QuerySet[Post]:
        following_queryset = UserFollowing.objects.filter(
            user_id=self.request.user
        )
        following_users_ids = [
            user.following_user_id.id for user in following_queryset
        ]
        queryset = (
            Post.objects.filter(
                Q(user_id__in=following_users_ids) | Q(user=self.request.user)
            )
            .prefetch_related("commentaries__user")
            .select_related("user")
        )
        hashtag = self.request.query_params.get("hashtag")

        if hashtag:
            queryset = queryset.filter(content__icontains=hashtag)

        return queryset

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action in ("list", "retrieve"):
            return PostListSerializer

        return super().get_serializer_class()

    def perform_create(
        self,
        serializer: Serializer,
    ) -> None:
        serializer.save(user=self.request.user)

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
        return Response("You liked this post", status=status.HTTP_200_OK)

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
    def comment(self, request: Request, pk: Optional[int] = None) -> Response:
        """Creates comment"""

        post = self.get_object()
        commentary = request.data.get("commentary")
        comm = Commentary.objects.create(
            commentary=commentary, post=post, user=self.request.user
        )
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
    def remove(self, request: Request, pk: Optional[int] = None) -> Response:
        """Deletes all own commentaries"""

        commentaries = self.get_object().commentaries.filter(
            user_id=self.request.user.id
        )
        if len(commentaries) > 0:
            commentaries.delete()
            return Response(
                "All my commentaries deleted", status=status.HTTP_200_OK
            )

        return Response("You have no comments", status=status.HTTP_200_OK)

    @action(
        methods=["GET"],
        detail=False,
        url_path="liked",
    )
    def liked(self, request: Request, pk: Optional[int] = None) -> Response:
        """Liked posts"""

        queryset = self.filter_queryset(self.get_queryset()).filter()
        like_qs = [
            _
            for _ in queryset
            if list(_.likes.values("user_id")) != []
            if self.request.user.id
            in sum(list(_.likes.values_list("user_id")), ())
        ]
        page = self.paginate_queryset(like_qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(like_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="hashtag",
                description="Filter by hashtag insensitive contains (ex. ?hashtag=post)",
                type=OpenApiTypes.STR,
            ),
        ]
    )
    def list(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """List characters with filter by hashtag"""
        return super().list(request, *args, **kwargs)


class CommentaryViewSet(generics.ListAPIView):
    """Commentary CRUD endpoints"""

    serializer_class = CommentarySerializer

    def get_queryset(self) -> QuerySet[Commentary]:
        return Commentary.objects.filter(
            user_id=self.request.user.id
        ).select_related("post", "user")
