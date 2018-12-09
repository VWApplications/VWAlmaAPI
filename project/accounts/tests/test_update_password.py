from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from accounts.serializers import UserPasswordSerializer


class UpdateUserPasswordTestCase(APITestCase):
    """
    Unit test case to test update a user password in the system.
    BUG: Tentar verificar as credenciais sem precisar forçar autenticação.
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
        self.url = reverse('user-change-password', kwargs={'pk': self.user.pk})

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.superuser.delete()
        self.client.logout()
        self.user.delete()

    def test_valid_update_user_password(self):
        """
        Test to update the own user password.
        """

        data = {
            'password': self.user.password,
            'new_password': 'pedro123456789',
            'confirm_password': 'pedro123456789'
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_user_old_password(self):
        """
        Test to can't update a user password. new passwords doesn't match.
        """

        data = {
            'password': 'password-invalido',
            'new_password': 'pedro123456789',
            'confirm_password': 'pedro123456789'
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            [_('Old password invalid.')]
        )

    def test_invalid_update_user_new_password(self):
        """
        Test to can't update a user password. new passwords doesn't match.
        """

        data = {
            'password': self.user.password,
            'new_password': 'pedro12345678',
            'confirm_password': 'pedro123456789'
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            [_('The new passwords do not match.')]
        )

    def test_invalid_update_another_user_password(self):
        """
        Can't Update another user password of system.
        """

        url = reverse('user-change-password', kwargs={'pk': self.superuser.pk})
        data = UserPasswordSerializer(self.superuser).data
        data.update({
            'password': 'victorhad123456',
            'new_password': 'pedro123456789',
            'confirm_password': 'pedro123456789'
        })
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_password_not_found(self):
        """
        Test to find user password that not exists.
        """

        url_invalid = reverse('user-change-password', kwargs={'pk': 30})
        data = UserPasswordSerializer(self.user).data
        data.update({
            'password': 'pedro123456',
            'new_password': 'pedro123456789',
            'confirm_password': 'pedro123456789'
        })
        response = self.client.put(url_invalid, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
