from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from another_todo_list.models import Task, Category
from datetime import timedelta
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, timezone
from another_todo_list.serializers import TaskSerializer


class TaskViewSetTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category', owner=self.user)

        self.task_data = {
            'category': self.category,
            'title': 'Test Task',
            'completed': False,
            'due_to': datetime.now(timezone.utc) + timedelta(days=1),
            'description': "Test description"
        }

        self.task = Task.objects.create(owner=self.user, **self.task_data)
        self.client = APIClient()
        self.list_url = reverse('task-list')
        self.detail_url = reverse('task-detail', args=[self.task.id])

    def test_unauthenticated_user_create_task(self):
        data = {
            'category': self.category.id,
            'title': 'New Task',
            'completed': False,
            'due_to': datetime.now(timezone.utc) + timedelta(days=2),
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Task.objects.count(), 1)

    def test_authenticated_user_create_task(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'category': self.category.id,
            'title': 'New Task',
            'completed': False,
            'due_to': datetime.now(timezone.utc) + timedelta(days=2),
            'description': 'New Description'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.last().title, 'New Task')

    def test_unauthenticated_user_update_task(self):
        data = {'title': 'Updated Task'}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Task.objects.get(id=self.task.id).title, 'Test Task')

    def test_authenticated_user_update_task(self):
        self.client.force_authenticate(user=self.user)

        data = {'title': 'Updated Task', 'description': 'Updated Description'}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(id=self.task.id).title, 'Updated Task')

    def test_unauthenticated_user_delete_task(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Task.objects.count(), 1)

    def test_authenticated_user_delete_task(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_task_serializer_validation_due_to_future_date(self):
        data = {
            'category': self.category.id,
            'title': 'Task with Future Due Date',
            'completed': False,
            'due_to': datetime.now(timezone.utc) + timedelta(days=1),
            'description': 'Test description'
        }

        serializer = TaskSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_task_serializer_validation_due_to_past_date(self):
        data = {
            'category': self.category.id,
            'title': 'Task with Past Due Date',
            'completed': False,
            'due_to': datetime.now(timezone.utc) - timedelta(days=1),
            'description': 'Test description'
        }

        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('due_to', serializer.errors)
        self.assertEqual(serializer.errors['due_to'][0], 'Due to date must be greater than creation data')
