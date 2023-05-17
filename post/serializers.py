from rest_framework import serializers

from post.models import Post, Commentary


class PostSerializer(serializers.ModelSerializer):
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
    user = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="email"
    )


class PostDetailSerializer(PostSerializer):
    commentaries = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="commentary"
    )
    user = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="email"
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "create_date",
            "content",
            "total_likes",
            "commentaries",
            "image",
            "user",
        )


class LikePostSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ("id",)


class CommentarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentary
        fields = (
            "id",
            "commentary",
        )


class CommentaryRemoveSerializer(CommentarySerializer):
    class Meta:
        model = Commentary
        fields = ("id",)
