from django.contrib.contenttypes.models import ContentType

from user.models import User
from .models import Like, Post


def add_like(obj: Post, user: User) -> Like:
    """Likes `obj`."""

    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = Like.objects.get_or_create(
        content_type=obj_type, object_id=obj.id, user=user
    )
    return like


def remove_like(obj: Post, user: User) -> None:
    """Deletes like from `obj`."""

    obj_type = ContentType.objects.get_for_model(obj)
    Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user
    ).delete()
