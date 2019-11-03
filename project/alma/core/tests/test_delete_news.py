from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from alma.core.models import News


class DeleteNewsTestCase(APITestCase):
    """
    Unit test responsible for delete news.
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
            description='News description...'
        )
        self.url = reverse('new-detail', kwargs={'pk': self.news.pk})

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.superuser.delete()
        self.client.logout()
        self.user.delete()
        self.news.delete()

    def test_valid_delete_news(self):
        """
        Delete news with superuser.
        """

        self.client.force_authenticate(self.superuser)
        self.assertEqual(News.objects.count(), 1)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(News.objects.count(), 0)

    def test_invalid_delete_news(self):
        """
        User that not superuser can't delete news.
        """

        self.client.force_authenticate(self.user)
        self.assertEqual(News.objects.count(), 1)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(News.objects.count(), 1)

    def test_not_find_news_to_delete(self):
        """
        Can't find news to delete, invalid url.
        """

        self.client.force_authenticate(self.superuser)
        url_invalid = reverse('new-detail', kwargs={'pk': 30})
        self.assertEqual(News.objects.count(), 1)
        response = self.client.delete(url_invalid)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(News.objects.count(), 1)
