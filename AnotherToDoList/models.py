from django.db.models import Model, CharField, IntegerField, BooleanField, DateTimeField, ForeignKey, CASCADE, SET_NULL, ManyToManyField
from django.contrib.auth.models import User


class Category(Model):
    name = CharField(max_length=250, unique=True)
    owner = ForeignKey(User, on_delete=CASCADE)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Task(Model):
    title = CharField(max_length=250)
    description = CharField(max_length=500)
    completed = BooleanField(default=False)
    category = ForeignKey(Category, on_delete=SET_NULL, default=None, null=True)
    owner = ForeignKey(User, on_delete=CASCADE)
    creation_date = DateTimeField(auto_now=True, editable=False) # ?????
    due_to = DateTimeField(default=None, null=True)  #?????

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

        ordering = ['creation_date']
        unique_together = ['title', 'description']

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title


class ToDoList(Model):
    title = CharField(max_length=250, unique=True)
    tasks = ManyToManyField(Task)

    class Meta:
        verbose_name = 'ToDoList'
        verbose_name_plural = 'ToDoLists'

    def __str__(self):
        return self.title
