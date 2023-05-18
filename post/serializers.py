from rest_framework import serializers

from post.models import Post, Commentary


class CommentarySerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="email",
    )

    class Meta:
        model = Commentary
        fields = (
            "id",
            "post",
            "user",
            "commentary",
        )
        read_only_fields = ("user", "post")


class CommentaryRemoveSerializer(CommentarySerializer):
    class Meta:
        model = Commentary
        fields = ("id",)


class PostSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="email",
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "create_date",
            "content",
            "total_likes",
            "image",
            "user",
        )


class PostListSerializer(PostSerializer):
    commentaries = CommentarySerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "create_date",
            "content",
            "total_likes",
            "image",
            "user",
            "commentaries",
        )


class LikePostSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ("id",)
