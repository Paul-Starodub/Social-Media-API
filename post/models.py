from __future__ import annotations
import os
import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRelation,
)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify


def movie_image_file_path(instance: Post, filename: str) -> str:
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.content[:10])}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/movies/posts/", filename)


class Like(models.Model):
    """Like model"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="likes",
        on_delete=models.CASCADE,
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")


class Post(models.Model):
    """Post model"""

    create_date = models.DateField(auto_now=True)
    content = models.CharField(max_length=280)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="posts",
    )
    likes = GenericRelation(Like)
    image = models.ImageField(
        null=True, blank=True, upload_to=movie_image_file_path
    )

    def __str__(self) -> str:
        return self.content[:25]

    @property
    def total_likes(self) -> int:
        return self.likes.count()

    class Meta:
        ordering = ["-create_date"]


class Commentary(models.Model):
    commentary = models.CharField(max_length=350)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="commentaries"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="commentaries",
    )

    def __str__(self) -> str:
        return self.commentary[:14]
