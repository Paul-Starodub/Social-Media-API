from django.views import View
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request

from user.models import UserFollowing


class IsAuthenticatedOrAnonymous(BasePermission):
    """Permissions for authorized/unauthorized users"""

    def has_permission(self, request: Request, view: View) -> bool:
        if (
            not request.user.is_authenticated
            and request.method not in SAFE_METHODS
        ):
            return True
        if request.user.is_authenticated and request.method in SAFE_METHODS:
            return True


class IsOwnerFollowing(BasePermission):
    """Permissions for users owners"""

    def has_object_permission(
        self, request: Request, view: View, obj: UserFollowing
    ) -> bool:
        if request.method in SAFE_METHODS:
            return True

        return obj.user_id == request.user
