from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework import generics, viewsets
from rest_framework.serializers import Serializer

from user.models import User, UserFollowing
from user.permissions import IsAuthenticatedOrAnonymous
from user.serializers import (
    UserSerializer,
    FollowingSerializer,
)


class CreateUserView(generics.ListCreateAPIView):
    """Create new user"""

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrAnonymous,)

    def get_queryset(self) -> QuerySet:
        queryset = get_user_model().objects.all()
        nickname = self.request.query_params.get("nickname")

        if self.request.user.is_authenticated and nickname:
            queryset = queryset.filter(nickname=nickname)

        return queryset


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    """Update user witch already login"""

    serializer_class = UserSerializer

    def get_object(self) -> User:
        return self.request.user


class RetrieveUserView(generics.RetrieveAPIView):
    """Retrieve user witch already login"""

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserFollowingViewSet(viewsets.ModelViewSet):
    """Following users"""

    serializer_class = FollowingSerializer
    queryset = UserFollowing.objects.all()

    def perform_create(self, serializer: Serializer) -> None:
        serializer.save(user_id=self.request.user)
