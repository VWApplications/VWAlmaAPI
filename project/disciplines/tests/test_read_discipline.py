from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from disciplines.models import Discipline
from disciplines.serializers import DisciplineSerializer
from django.contrib.auth import get_user_model

# Get the custom user from settings
User = get_user_model()


class ReadDisciplineTestCase(APITestCase):
    """
    Test to show all or a single discipline of the system.
    """

    def setUp(self):
        """
        This method will run before any test.
        """

        self.teacher = User.objects.create(
            name='Teacher 01',
            email='teacher@gmail.com',
            is_teacher=True,
            password='123456'
        )
        self.discipline = Discipline.objects.create(
            title="Discipline 01",
            description="Description 01",
            course="Course 01",
            teacher=self.teacher
        )
        self.student = User.objects.create(
            name='Student 01',
            email='student@gmail.com',
            password='123456'
        )
        self.url = reverse(
            'discipline-detail',
            kwargs={'pk': self.discipline.pk}
        )

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.client.logout()
        self.teacher.delete()
        self.student.delete()
        self.discipline.delete()

    def test_valid_not_logged_discipline_list(self):
        """
        Test found the discipline list not logged.
        """

        disciplines = Discipline.objects.all()
        serializer = DisciplineSerializer(disciplines, many=True)
        url = reverse('discipline-list')
        response = self.client.get(url)
        self.assertEqual(Discipline.objects.count(), 1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_logged_discipline_list(self):
        """
        Test found the discipline list logged.
        """

        self.client.force_authenticate(self.teacher)
        disciplines = Discipline.objects.all()
        serializer = DisciplineSerializer(disciplines, many=True)
        url = reverse('discipline-list')
        response = self.client.get(url)
        self.assertEqual(Discipline.objects.count(), 1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_logged_student_discipline_list(self):
        """
        Test found the discipline list by student.
        """

        self.client.force_authenticate(self.student)
        disciplines = Discipline.objects.all()
        serializer = DisciplineSerializer(disciplines, many=True)
        url = reverse('discipline-list')
        response = self.client.get(url)
        self.assertEqual(Discipline.objects.count(), 1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_own_discipline_detail(self):
        """
        Test found the own discipline.
        """

        self.client.force_authenticate(self.teacher)
        serializer = DisciplineSerializer(self.discipline)
        response = self.client.get(self.url)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_not_logged_discipline_detail(self):
        """
        Test found the discipline without be logged.
        """

        serializer = DisciplineSerializer(self.discipline)
        response = self.client.get(self.url)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_student_read_discipline_detail(self):
        """
        Test student found the discipline.
        """

        self.client.force_authenticate(self.student)
        serializer = DisciplineSerializer(self.discipline)
        response = self.client.get(self.url)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_another_discipline_detail(self):
        """
        Test found the specific discipline.
        """

        self.teacher2 = User.objects.create(
            name='Teacher 02',
            email='teacher02@gmail.com',
            is_teacher=True,
            password='123456'
        )
        self.discipline2 = Discipline.objects.create(
            title="Discipline 02",
            description="Description 02",
            course="Course 02",
            teacher=self.teacher2
        )
        self.client.force_authenticate(self.teacher)
        url = reverse('discipline-detail', kwargs={'pk': self.discipline2.id})
        serializer = DisciplineSerializer(self.discipline2)
        response = self.client.get(url)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_url_discipline_detail(self):
        """
        Test to not found the specific discipline.
        """

        url_invalid = reverse('discipline-detail', kwargs={'pk': 30})
        response = self.client.get(url_invalid)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
