from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from another_todo_list.models import ToDoList, Category, Task
from django.contrib.auth.models import User
from django.urls import reverse


class ToDoListViewSetTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.category = Category.objects.create(name='Test Category', owner=self.user)

        # Create a test task
        self.task = Task.objects.create(
            category=self.category,
            title='Test Task',
            completed=False,
            due_to='2024-02-28',
            description='Test Description',
            owner=self.user
        )
        self.todolist_data = {'title': 'Test ToDoList'}
        self.todolist = ToDoList.objects.create(**self.todolist_data, owner=self.user)
        self.todolist.tasks.add(self.task)

        self.client = APIClient()

        self.list_url = reverse('todos-list')
        self.detail_url = reverse('todos-detail', args=[self.todolist.id])

    def test_unauthenticated_user_list_todolists(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_retrieve_todolist(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_list_todolists(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test ToDoList')

    def test_authenticated_user_retrieve_todolist(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test ToDoList')

    def test_unauthenticated_user_create_todolist(self):
        data = {'title': 'New ToDoList'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_create_todolist(self):
        self.client.force_authenticate(user=self.user)
        data = {'title': 'New ToDoList'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ToDoList.objects.last().title, 'New ToDoList')
        self.assertEqual(ToDoList.objects.last().owner, self.user)

    def test_unauthenticated_user_update_todolist(self):
        data = {'title': 'Updated ToDoList'}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(ToDoList.objects.get(id=self.todolist.id).title, 'Test ToDoList')

    def test_authenticated_user_update_todolist(self):
        self.client.force_authenticate(user=self.user)

        data = {'title': 'Updated ToDoList'}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ToDoList.objects.get(id=self.todolist.id).title, 'Updated ToDoList')

    def test_unauthenticated_user_delete_todolist(self):
        initial_count = ToDoList.objects.count()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(ToDoList.objects.count(), initial_count)

    def test_authenticated_user_delete_todolist(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ToDoList.objects.count(), 0)
