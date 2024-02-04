from django.contrib import admin
from another_todo_list.models import Category, Task, ToDoList
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth.admin import UserAdmin


class CustomAdminSite(admin.AdminSite):
    site_header = 'ToDo List Administration'
    site_title = 'ToDo List Administration'
    index_title = 'Hello'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    search_fields = ('name', 'owner__username')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'completed', 'category', 'owner', 'creation_date', 'due_to')
    list_filter = ('completed', 'category', 'owner', 'creation_date', 'due_to')
    search_fields = ('title', 'description', 'owner__username')
    date_hierarchy = 'creation_date'
    ordering = ('creation_date',)


class ToDoListAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_task_count')
    search_fields = ('title',)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(task_count=Count('tasks'))

    def get_task_count(self, obj):
        return obj.task_count

    get_task_count.short_description = 'Task Count'


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')
    ordering = ('-date_joined',)


custom_admin_site = CustomAdminSite(name='customadmin')
custom_admin_site.register(Category, CategoryAdmin)
custom_admin_site.register(Task, TaskAdmin)
custom_admin_site.register(ToDoList, ToDoListAdmin)
custom_admin_site.register(User, CustomUserAdmin)
