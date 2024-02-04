from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from another_todo_list.models import Category
from another_todo_list.serializers import CategorySerializer
from django.contrib.auth.models import User
from django.urls import reverse


class CategoryViewSetTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.category_data = {'name': 'Test Category'}
        self.category = Category.objects.create(owner=self.user, **self.category_data)

        self.client = APIClient()

        self.list_url = reverse('category-list')
        self.detail_url = reverse('category-detail', args=[self.category.id])

    def test_unauthenticated_user_list_categories(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_retrieve_category(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_list_categories(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Category')

    def test_authenticated_user_retrieve_category(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Category')

    def test_unauthenticated_user_create_category(self):
        data = {'name': 'New Category'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_create_category(self):
        self.client.force_authenticate(user=self.user)

        data = {'name': 'New Category'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.last().name, 'New Category')

    def test_unauthenticated_user_update_category(self):
        data = {'name': 'Updated Category'}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_update_category(self):
        self.client.force_authenticate(user=self.user)

        data = {'name': 'Updated Category'}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.get(id=self.category.id).name, 'Updated Category')

    def test_unauthenticated_user_delete_category(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_delete_category(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)
