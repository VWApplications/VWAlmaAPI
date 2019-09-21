from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User


class LoginTestCase(APITestCase):
    """
    Unit test case to test the login to the system.
    The loggin system are already tested in package djangorest-jwt
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
        self.url = reverse('user-detail', kwargs={'pk': self.user.pk})

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.superuser.delete()
        self.client.logout()
        self.user.delete()

    def test_logged(self):
        """
        Verify if user are authenticated.
        """

        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_not_logged(self):
        """
        Verify if user are not authenticated.
        """

        response = self.client.get(self.url)
        self.assertTrue(not response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
