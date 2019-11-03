from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from alma.core.models import News


class UpdateNewsTestCase(APITestCase):
    """
    Unit test case to test update news in the system.
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
        self.news = News.objects.create(
            title='News title',
            description='News description...',
            link=""
        )
        self.data = {
            'title': 'Título',
            'description': 'Description',
            'link': 'http://www.google.com',
            'tags': []
        }
        self.url = reverse('new-detail', kwargs={'pk': self.news.pk})

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.superuser.delete()
        self.client.logout()
        self.user.delete()
        self.news.delete()

    def test_valid_update_news(self):
        """
        Test to admin update the news.
        """

        self.client.force_authenticate(self.superuser)
        self.data['title'] = "News 1"
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_news(self):
        """
        Only superuser can update news.
        """

        self.client.force_authenticate(self.user)
        self.data['description'] = "Important news..."
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_update_news_without_title(self):
        """
        Can't Update news with title empty.
        """

        self.client.force_authenticate(self.superuser)
        self.data['title'] = ""
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_update_news_without_description(self):
        """
        Can't Update news with description empty.
        """

        self.client.force_authenticate(self.superuser)
        self.data['description'] = ""
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_news_not_found(self):
        """
        Test to find news that not exists.
        """

        self.client.force_authenticate(self.superuser)
        url_invalid = reverse('new-detail', kwargs={'pk': 30})
        self.data['title'] = "News 1"
        response = self.client.put(url_invalid, self.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
