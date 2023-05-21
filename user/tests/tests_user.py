import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from user.serializers import UserSerializer

USERS_URL = reverse("users:create")


class UnAuthenticatedUserApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        response = self.client.get(USERS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.client2 = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email="test1@gmail.com",
            password="555qaz",
            nickname="red",
            is_staff=True,
            date_of_birth=datetime.date(2012, 2, 12),
        )
        self.client.force_authenticate(self.user)
        self.user2 = get_user_model().objects.create_user(
            email="test2@gmail.com",
            password="555qaz",
            nickname="green",
            is_staff=True,
            date_of_birth=datetime.date(2012, 2, 12),
        )
        self.client2.force_authenticate(self.user2)

    def test_create_superuser_and_user(self) -> None:
        admin = get_user_model().objects.create_superuser(
            email="test@gmail.com",
            password="555qaz",
            nickname="blue",
            is_staff=True,
            date_of_birth=datetime.date(2012, 2, 12),
        )
        user = UserSerializer().create(
            validated_data={
                "email": "test5@gmail.com",
                "password": "555qaz",
                "is_staff": False,
                "date_of_birth": datetime.date(2012, 2, 12),
                "nickname": "white",
            }
        )

        self.assertTrue(admin.is_superuser)
        self.assertFalse(user.is_staff)

    def test_user_password(self) -> None:
        test_user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="555qaz",
            nickname="yellow",
            date_of_birth=datetime.date(2012, 2, 12),
        )
        UserSerializer(test_user).update(
            test_user, validated_data={"password": "new_password"}
        )

        self.assertEquals(test_user.check_password("new_password"), True)

    def test_filter_users_by_is_nickname(self) -> None:
        serializer1 = UserSerializer(self.user)
        serializer2 = UserSerializer(self.user2)

        response = self.client.get(USERS_URL, params={"nickname": "green"})

        self.assertIn(serializer1.data, response.data)
        self.assertIn(serializer2.data, response.data)
