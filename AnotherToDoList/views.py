from rest_framework import viewsets
from AnotherToDoList.models import Category, Task, ToDoList
from AnotherToDoList.serializers import CategorySerializer, TaskSerializer, ToDoListSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from AnotherToDoList.permissions import IsOwnerOrReadOnly


class UserOwnedModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user)


class CategoryViewSet(UserOwnedModelViewSet):
    """Endpoint provides access to the list of categories for user tasks"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']


class TaskViewSet(UserOwnedModelViewSet):
    """Endpoint provides access to user tasks"""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'title', 'completed', 'due_to']


class ToDoListViewSet(UserOwnedModelViewSet):
    """Endpoint provides access to user to-do lists"""
    queryset = ToDoList.objects.all()
    serializer_class = ToDoListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title']
