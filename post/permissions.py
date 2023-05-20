from django.views import View
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request

from post.models import Post


class IsAuthenticatedOrAnonymous(BasePermission):
    """Permissions for authorized/unauthorized users"""

    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_authenticated

    def has_object_permission(self, request: Request, view: View, obj: Post) -> bool:
        if request.user.is_authenticated and view.action in (
            (
                "leave_comment",
                "like",
                "unlike",
                "remove_all_comments",
            )
            + SAFE_METHODS
        ):
            return True

        return obj.user == request.user
