from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from post.models import Post, Commentary
from post.serializers import PostSerializer

POSTS_URL = reverse("posts:post-list")


def detail_post_url(post_id: int) -> str:
    return reverse("posts:post-detail", kwargs={"pk": post_id})


class UnAuthenticatedPostApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        response = self.client.get(POSTS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_str_method(self) -> None:
        user = get_user_model().objects.create(
            email="user@gmail.com",
            nickname="user",
            date_of_birth="2012-01-01",
            password="test123",
        )
        post = Post.objects.create(content="test123456789123456789123456789", user=user)
        self.assertEqual(str(post), "test123456789123456789123")


class AuthenticatedPostApiTests(TestCase):
    def setUp(self) -> None:
        self.client1 = APIClient()
        self.client2 = APIClient()
        self.user1 = get_user_model().objects.create_user(
            email="user1@gmail.com",
            nickname="user1",
            date_of_birth="2012-01-01",
            password="test1",
        )
        self.user2 = get_user_model().objects.create_user(
            email="user2@gmail.com",
            nickname="user2",
            date_of_birth="2012-01-01",
            password="test2",
        )
        self.client1.force_authenticate(self.user1)
        self.client2.force_authenticate(self.user2)

    def test_list_posts(self) -> None:
        Post.objects.create(content="test123456789123456789123456789", user=self.user1)
        Post.objects.create(content="test123456789123456789123456789", user=self.user2)

        response = self.client1.get(POSTS_URL)
        posts = Post.objects.all()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(posts), 2)

    def test_retrieve_post_detail(self) -> None:
        post = Post.objects.create(
            content="test123456789123456789123456789", user=self.user1
        )

        url = detail_post_url(post.pk)
        response = self.client1.get(url)
        serializer = PostSerializer(post)
        response.data.pop("commentaries")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(serializer.data, response.data)

    def test_create_comment(self) -> None:
        post = Post.objects.create(
            content="test123456789123456789123456789", user=self.user1
        )
        commentary = "About post"
        payload = {"commentary": commentary}
        url = reverse("posts:post-comment", kwargs={"pk": post.id})
        response = self.client1.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_comment(self) -> None:
        post = Post.objects.create(
            content="test123456789123456789123456789", user=self.user1
        )
        Commentary.objects.create(commentary="About us", post=post, user=self.user1)
        url = reverse("posts:post-remove", kwargs={"pk": post.id})
        response = self.client1.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_post(self) -> None:
        post = Post.objects.create(
            content="test123456789123456789123456789", user=self.user1
        )
        url = reverse("posts:post-like", kwargs={"pk": post.id})
        response = self.client1.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unlike_post(self) -> None:
        post = Post.objects.create(
            content="test123456789123456789123456789", user=self.user1
        )
        url = reverse("posts:post-unlike", kwargs={"pk": post.id})
        response = self.client1.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_liked_posts(self) -> None:
        post1 = Post.objects.create(
            content="test123456789123456789123456789", user=self.user1
        )
        post2 = Post.objects.create(
            content="test123456789123456789120000000003456789", user=self.user1
        )
        url1 = reverse("posts:post-like", kwargs={"pk": post1.id})
        url2 = reverse("posts:post-like", kwargs={"pk": post2.id})
        self.client1.post(url1)
        self.client1.post(url2)
        url = reverse("posts:post-liked")

        response = self.client1.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
