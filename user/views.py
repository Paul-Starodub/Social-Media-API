from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.permissions import AllowAny


from user.models import User
from user.serializers import UserSerializer


class CreateUserView(generics.ListCreateAPIView):
    """Create new user"""

    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self) -> QuerySet:
        queryset = get_user_model().objects.all()
        nickname = self.request.query_params.get("nickname")

        if self.request.user.is_authenticated:
            queryset = queryset.filter(nickname=nickname)

        return queryset


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    """Update user witch already login"""

    serializer_class = UserSerializer

    def get_object(self) -> User:
        return self.request.user
