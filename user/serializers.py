import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from user.models import User, UserFollowing


class FollowingSerializer(serializers.ModelSerializer):
    user_id = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="email",
        queryset=User.objects.all(),
    )
    following_user_id = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="email",
        queryset=User.objects.all(),
    )

    class Meta:
        model = UserFollowing
        fields = ("id", "user_id", "following_user_id", "created")
        read_only_fields = ("created", "user_id")
        validators = [
            UniqueTogetherValidator(
                queryset=UserFollowing.objects.all(),
                fields=["user_id", "following_user_id"],
            )
        ]


class FollowersSerializer(serializers.ModelSerializer):
    user_id = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="email",
        queryset=User.objects.all(),
    )

    class Meta:
        model = UserFollowing
        fields = ("id", "user_id", "created")


class UserSerializer(serializers.ModelSerializer):
    following = FollowingSerializer(many=True, read_only=True)
    followers = FollowersSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "is_staff",
            "nickname",
            "biography",
            "date_of_birth",
            "profile_image",
            "following",
            "followers",
        )
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data: dict) -> User:
        """Create a new user with encrypted password and return it"""

        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        """Update a user, set the password correctly and return it"""

        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user

    def validate_date_of_birth(
        self, value: datetime.date
    ) -> ValidationError | datetime.date:
        if not value:
            raise serializers.ValidationError("You must indicate your age!")

        if value > datetime.date.today() - datetime.timedelta(weeks=260):
            raise serializers.ValidationError(
                "You must be at least 5 years old!"
            )

        return value
