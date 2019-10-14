from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from accounts.enum import PermissionSet
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User


class CreateUserTestCase(APITestCase):
    """
    Unit test case to test creating new users in the system.
    """

    def setUp(self):
        """
        This method will run before any test.
        """

        self.superuser = User.objects.create_superuser(
            name='Victor Arnaud',
            permission=PermissionSet.TEACHER.value,
            email='victorhad@gmail.com',
            password='victorhad123456'
        )
        self.user = User.objects.create(
            name='Pedro Calile',
            email='pedro@gmail.com',
            password='pedro123456'
        )
        self.data = {
            'name': 'Fulano de Tal',
            'permission': PermissionSet.TEACHER.value,
            'email': 'fulano@gmail.com',
            'password': 'fulano123456',
            'confirm_password': 'fulano123456'
        }
        self.url = reverse('user-list')

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.superuser.delete()
        self.user.delete()

    def test_valid_create_teacher_user(self):
        """
        Create a new user in the system.
        """

        self.assertEqual(User.objects.count(), 2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_valid_create_student_user(self):
        """
        Create a new user in the system.
        """

        self.assertEqual(User.objects.count(), 2)
        self.data['permission'] = PermissionSet.STUDENT.value
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_invalid_same_email_created_user(self):
        """
        Can't create a user with same email address.
        """

        self.assertEqual(User.objects.count(), 2)
        self.data['email'] = "pedro@gmail.com"
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)

    def test_invalid_email_create_user(self):
        """
        Can't create a new user in the system, because of invalid email.
        """

        self.assertEqual(User.objects.count(), 2)
        self.data['email'] = ""
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(
            response.data,
            {'email': [_('This field may not be blank.')]}
        )

    def test_invalid_password_create_user(self):
        """
        Can't create a new user in the system, because of invalid password.
        """

        self.assertEqual(User.objects.count(), 2)
        self.data['confirm_password'] = "password errado"
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(
            response.data['detail'],
            _("The passwords do not match.")
        )
