from django.views import View
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request

from post.models import Post


class IsAuthenticatedOrAnonymous(BasePermission):
    """Permissions for authorized/unauthorized users"""

    def has_permission(self, request: Request, view: View) -> bool:
        if request.user.is_anonymous:
            return False
        return True

    def has_object_permission(
        self, request: Request, view: View, obj: Post
    ) -> bool:
        if request.user.is_authenticated and view.action in (
            "leave_comment",
            "like",
            "unlike",
            "remove_all_comments",
        ):
            return True
        if request.user.is_authenticated and request.method in SAFE_METHODS:
            return True

        return obj.user == request.user
