from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from disciplines.models import Discipline
from django.contrib.auth import get_user_model

# Get the custom user from settings
User = get_user_model()


class UpdateDisciplineTestCase(APITestCase):
    """
    Unit test case to test a discipline's update on the system
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
        self.data = {
            'title': "Discipline 02",
            'description': "Description 01",
            'institution': "Institution 01",
            'course': "Course 01",
            'classroom': 'Class A',
            'password': 'turma1234',
            'students_limit': 10,
            'monitors_limit': 3,
            'is_closed': False
        }
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

    def test_valid_update_discipline(self):
        """
        Test to update the own discipline.
        """

        self.client.force_authenticate(self.teacher)
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Discipline 02')

    def test_invalid_update_discipline_by_not_logged_teacher(self):
        """
        Test to update discipline by not logged user.
        """

        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_update_by_student(self):
        """
        Only teacher can update discipline
        """

        self.client.force_authenticate(self.student)
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_description_update_discipline(self):
        """
        Test can't update a specific discipline. Invalid description.
        """

        self.client.force_authenticate(self.teacher)
        self.data['description'] = ""
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'description': [_('This field may not be blank.')]}
        )

    def test_invalid_title_update_discipline(self):
        """
        Test can't update a specific discipline. Invalid title.
        """

        self.client.force_authenticate(self.teacher)
        self.data['title'] = ""
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'title': [_('This field may not be blank.')]}
        )

    def test_invalid_course_update_discipline(self):
        """
        Test can't update a specific discipline. Invalid course.
        """

        self.client.force_authenticate(self.teacher)
        self.data['course'] = ""
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'course': [_('This field may not be blank.')]}
        )

    def test_invalid_update_another_discipline(self):
        """
        Can't Update another teacher discipline of system.
        """

        self.teacher2 = User.objects.create(
            name='Teacher 02',
            email='teacher02@gmail.com',
            is_teacher=True,
            password='123456'
        )
        self.client.force_authenticate(self.teacher2)
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_discipline_not_found(self):
        """
        Test to find discipline that not exists.
        """

        url_invalid = reverse('discipline-detail', kwargs={'pk': 30})
        response = self.client.put(url_invalid, self.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
