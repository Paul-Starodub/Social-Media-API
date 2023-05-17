from __future__ import annotations

import datetime
import os
import uuid
from typing import Any, Optional

from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(
        self, email: str, password: str, **extra_fields: dict[str, Any]
    ) -> ValueError | User:
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        email: str,
        password: Optional[str] = None,
        **extra_fields: dict[str, Any],
    ) -> User:
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self, email: str, password: str, **extra_fields: dict[str, Any]
    ) -> ValueError | User:
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


def movie_image_file_path(instance: User, filename: str) -> str:
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.email)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/movies/users/", filename)


class User(AbstractUser):
    """A model for User."""

    username = None
    nickname = models.CharField(_("nickname"), max_length=15, unique=True)
    date_of_birth = models.DateField(_("date of birth"))
    biography = models.CharField(
        _("short biography"), max_length=400, blank=True, null=True
    )
    email = models.EmailField(_("email address"), unique=True)
    profile_image = models.ImageField(
        null=True, blank=True, upload_to=movie_image_file_path
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname", "date_of_birth"]

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    date_of_birth__lte=datetime.date.today()
                    - datetime.timedelta(weeks=260)
                ),
                name="You must be at least 5 years old!",
            )
        ]

    objects = UserManager()
