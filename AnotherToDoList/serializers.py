from datetime import datetime, timezone
from rest_framework.serializers import ModelSerializer, ValidationError
from AnotherToDoList.models import Category, Task, ToDoList


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        exclude = ['owner']


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        exclude = ['owner']

    def validate(self, attrs):
        if attrs.get('due_to') is not None:
            if attrs['due_to'] < datetime.now(timezone.utc):
                raise ValidationError("Due to date must be greater than creation data")
        return attrs


class ToDoListSerializer(ModelSerializer):
    class Meta:
        model = ToDoList
        fields = "__all__"
