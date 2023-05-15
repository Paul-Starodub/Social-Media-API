from django.conf import settings
from django.db import models


class Post(models.Model):
    """Post model"""
    create_date = models.DateField(auto_now=True)
    content = models.CharField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="posts",
    )
    commentary = models.CharField(max_length=250, null=True, blank=True)
    count_like = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.content[:25]

    class Meta:
        ordering = ["-create_date"]

