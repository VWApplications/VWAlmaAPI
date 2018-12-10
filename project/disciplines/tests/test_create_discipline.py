from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from disciplines.models import Discipline
from django.contrib.auth import get_user_model

# Get the custom user from settings
User = get_user_model()


class CreateDisciplineTestCase(APITestCase):
    """
    Unit test case to test creating new disciplines in the system.
    """

    def setUp(self):
        """
        This method will run before any test.
        """

        self.teacher = User.objects.create(
            name='Professor',
            email='professor@gmail.com',
            is_teacher=True,
            password='123456'
        )

        self.student = User.objects.create(
            name='Estudante',
            email='estudante@gmail.com',
            password='123456'
        )

        self.data = {
            'title': "Discipline 01",
            'description': "Description 01",
            'institution': "Institution",
            'course': "Course 01",
            'classroom': 'Class A',
            'password': 'turma1234',
            'students_limit': 10,
            'monitors_limit': 3,
            'is_closed': False
        }

        self.url = reverse('discipline-list')

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.client.logout()
        self.teacher.delete()
        self.student.delete()

    def test_valid_create_discipline(self):
        """
        Create a new discipline by teacher in the system.
        """

        self.client.force_authenticate(self.teacher)
        self.assertEqual(Discipline.objects.count(), 0)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Discipline.objects.count(), 1)

    def test_student_create_discipline(self):
        """
        Try to create a discipline by student.
        """

        self.client.force_authenticate(self.student)
        self.assertEqual(Discipline.objects.count(), 0)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Discipline.objects.count(), 0)

    def test_not_logged_create_discipline(self):
        """
        Try to create a discipline without be logged.
        """

        self.assertEqual(Discipline.objects.count(), 0)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Discipline.objects.count(), 0)

    def test_invalid_empty_title_create_discipline(self):
        """
        Try to create a discipline without title
        """

        self.client.force_authenticate(self.teacher)
        self.assertEqual(Discipline.objects.count(), 0)
        self.data['title'] = ""
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Discipline.objects.count(), 0)
        self.assertEqual(
            response.data,
            {'title': [_('This field may not be blank.')]}
        )

    def test_invalid_empty_description_create_discipline(self):
        """
        Tr to create a discipline without title
        """

        self.client.force_authenticate(self.teacher)
        self.assertEqual(Discipline.objects.count(), 0)
        self.data['description'] = ""
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Discipline.objects.count(), 0)
        self.assertEqual(
            response.data,
            {'description': [_('This field may not be blank.')]}
        )

    def test_invalid_empty_course_create_discipline(self):
        """
        Try to create a discipline without title
        """

        self.client.force_authenticate(self.teacher)
        self.assertEqual(Discipline.objects.count(), 0)
        self.data['course'] = ""
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Discipline.objects.count(), 0)
        self.assertEqual(
            response.data,
            {'course': [_('This field may not be blank.')]}
        )
