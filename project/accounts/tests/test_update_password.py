from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User


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
        self.user = User.objects.create_user(
            name='Pedro Calile',
            email='pedro@gmail.com',
            password='pedro123456'
        )
        self.client.force_authenticate(self.user)
        self.url = reverse('user-change-password')

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
            'password': 'pedro123456',
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
            response.data['detail'],
            "Senha antiga inválida."
        )

    def test_invalid_update_user_new_password(self):
        """
        Test to can't update a user password. new passwords doesn't match.
        """

        data = {
            'password': 'pedro123456',
            'new_password': 'pedro12345678',
            'confirm_password': 'pedro123456789'
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['detail'],
            "As novas senhas não combinam."
        )
