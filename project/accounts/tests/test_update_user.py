from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from accounts.serializers import UserSerializer


class UpdateUserTestCase(APITestCase):
    """
    Unit test case to test a user's update on the system
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
        self.data = {
            'name': "Fulano de tal",
            'email': "fulano@gmail.com"
        }
        self.client.force_authenticate(self.user)
        self.url = reverse('user-detail', kwargs={'pk': self.user.pk})

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.superuser.delete()
        self.client.logout()
        self.user.delete()

    def test_valid_update_user(self):
        """
        Test to update the own user.
        """

        self.data['name'] = "Pedro Masmorra"
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_user(self):
        """
        Test to can't update a specific user. Invalid email.
        """

        self.data['email'] = "fulano"
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'email': [_('Enter a valid email address.')]}
        )

    def test_invalid_update_another_user(self):
        """
        Can't Update another user of system.
        """

        url = reverse('user-detail', kwargs={'pk': self.superuser.pk})
        data = UserSerializer(self.superuser).data
        data.update({'email': 'fulano@gmail.com'})
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_not_found(self):
        """
        Test to find user that not exists.
        """

        url_invalid = reverse('user-detail', kwargs={'pk': 30})
        data = UserSerializer(self.user).data
        data.update({'email': 'fulano@gmail.com'})
        response = self.client.put(url_invalid, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
