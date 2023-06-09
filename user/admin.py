from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext as _

from .models import User, UserFollowing

admin.site.register(UserFollowing)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no username field."""

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "date_of_birth",
                    "biography",
                    "nickname",
                    "profile_image",
                )
            },
        ),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "date_of_birth",
                    "biography",
                    "nickname",
                ),
            },
        ),
    )
    list_display = ("email", "nickname", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name", "nickname")
    ordering = ("email",)
