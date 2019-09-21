from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from core.models import News


class CreateNewsTestCase(APITestCase):
    """
    Unit test case to test creating a news in the system.
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
        self.url = reverse('new-list')

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.superuser.delete()
        self.user.delete()

    # def test_valid_create_news(self):
    #     """
    #     Admin create a news in the system.
    #     """
    #
    #     self.client.force_authenticate(self.superuser)
    #     self.assertEqual(News.objects.count(), 0)
    #     data = {
    #         'title': 'News title',
    #         'description': 'News description...',
    #         'tags': [{"title": "Important"}]
    #     }
    #     response = self.client.post(self.url, data)
    #     print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(News.objects.count(), 1)

    def test_invalid_title_created_news(self):
        """
        Admin can't create a user without a title.
        """

        self.client.force_authenticate(self.superuser)
        self.assertEqual(News.objects.count(), 0)
        data = {
            'description': 'News description...',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(News.objects.count(), 0)

    def test_invalid_description_create_news(self):
        """
        Admin can't create a news without a description.
        """

        self.client.force_authenticate(self.superuser)
        self.assertEqual(News.objects.count(), 0)
        data = {
            'title': 'News title',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(News.objects.count(), 0)

    def test_invalid_user_not_admin_create_news(self):
        """
        Only admin can create a news.
        """

        self.client.force_authenticate(self.user)
        self.assertEqual(News.objects.count(), 0)
        data = {
            'title': 'News title',
            'description': 'News descriptions...',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(News.objects.count(), 0)
