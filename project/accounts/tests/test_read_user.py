from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from accounts.serializers import UserSerializer, UserRegisterSerializer


class ReadUserTestCase(APITestCase):
    """
    Test to show all or a single user of the system.
    """

    def setUp(self):
        """
        This method will run before any test.
        """

        self.superuser = User.objects.create_superuser(
            name='Victor Arnaud',
            email='victorhad@gmail.com',
            password='victorhad123456'
        )
        self.user = User.objects.create(
            name='Pedro Calile',
            email='pedro@gmail.com',
            password='pedro123456'
        )
        self.client.force_authenticate(self.user)

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.superuser.delete()
        self.client.logout()
        self.user.delete()

    def test_valid_user_list(self):
        """
        Test found the user list.
        """

        users = User.objects.all()
        serializer = UserRegisterSerializer(users, many=True)
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(User.objects.count(), 2)
        # self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_own_user_detail(self):
        """
        Test found the own user.
        """

        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        serializer = UserSerializer(self.user)
        response = self.client.get(url)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_another_user_detail(self):
        """
        Test found the specific user.
        """

        url = reverse('user-detail', kwargs={'pk': self.superuser.pk})
        serializer = UserSerializer(self.superuser)
        response = self.client.get(url)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_url_user_detail(self):
        """
        Test to not found the specific user.
        """

        url_invalid = reverse('user-detail', kwargs={'pk': 30})
        response = self.client.get(url_invalid)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
