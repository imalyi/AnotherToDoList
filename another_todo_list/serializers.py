from datetime import datetime, timezone
from rest_framework.serializers import ModelSerializer, ValidationError
from another_todo_list.models import Category, Task, ToDoList


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        exclude = ['owner']


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        exclude = ['owner']

    def validate_due_to(self, due_to):
        if due_to is not None:
            if due_to < datetime.now(timezone.utc):
                raise ValidationError("Due to date must be greater than creation data")
        return due_to


class ToDoListSerializer(ModelSerializer):
    class Meta:
        model = ToDoList
        exclude = ['owner']
