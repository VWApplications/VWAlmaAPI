from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from core.models import News
from core.serializers import NewsCreateTagsSerializer


class ReadNewsTestCase(APITestCase):
    """
    Test to show all news or a single news.
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
            title='News',
            description='News description...'
        )

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.superuser.delete()
        self.client.logout()
        self.user.delete()
        self.news.delete()

    def test_valid_news_list(self):
        """
        Test found the user list.
        """

        url = reverse('new-list')
        response = self.client.get(url)
        self.assertEqual(News.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_news_detail(self):
        """
        Test found the specific news.
        """

        url = reverse('new-detail', kwargs={'pk': self.news.pk})
        serializer = NewsCreateTagsSerializer(self.news)
        response = self.client.get(url)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_url_news_detail(self):
        """
        Test to not found the specific news.
        """

        url_invalid = reverse('new-detail', kwargs={'pk': 30})
        response = self.client.get(url_invalid)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
