from rest_framework.test import APITestCase
from accounts.models import User


class UserTestCase(APITestCase):
    """
    Unit test case to test user features.
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
        self.user1 = User.objects.create(
            name='Pedro',
            email='pedro@gmail.com',
            password='pedro123456'
        )
        self.user2 = User.objects.create(
            name='Maria de Fatima',
            email='maria@gmail.com',
            password='maria123456'
        )
        self.user3 = User.objects.create(
            name='Jose da Silva Pereira',
            email='jose@gmail.com',
            password='jose123456',
            photo='img/photo01.png'
        )

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.superuser.delete()
        self.user1.delete()
        self.user2.delete()
        self.user3.delete()

    def test_full_name(self):
        """
        Test to get the full name of user
        """

        self.assertEqual(self.superuser.full_name, self.superuser.name)
        self.assertEqual(self.user1.full_name, self.user1.name)
        self.assertEqual(self.user2.full_name, self.user2.name)
        self.assertEqual(self.user3.full_name, self.user3.name)

    def test_short_name(self):
        """
        Test to get the short name of user, the first name with the last name
        """

        self.assertEqual(self.superuser.short_name, 'Victor Arnaud')
        self.assertEqual(self.user1.short_name, self.user1.name)
        self.assertEqual(self.user2.short_name, 'Maria Fatima')
        self.assertEqual(self.user3.short_name, 'Jose Pereira')
