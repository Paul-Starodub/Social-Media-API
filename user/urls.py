from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.views import (
    CreateUserView,
    ManageUserView,
    UserFollowingViewSet,
    RetrieveUserView,
)

router = routers.DefaultRouter()
router.register("followings", UserFollowingViewSet, basename="following-list")

urlpatterns = [
    path("", CreateUserView.as_view(), name="create"),
    path("<int:pk>/", RetrieveUserView.as_view(), name="retrieve"),
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("me/", ManageUserView.as_view(), name="manage"),
]

app_name = "users"
