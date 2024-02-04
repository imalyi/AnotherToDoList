from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from another_todo_list.views import CategoryViewSet, TaskViewSet, ToDoListViewSet
from another_todo_list.admin import custom_admin_site
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="ToDo API",
      default_version='v1',
      description="API Documentation(ToDoList)",
      contact=openapi.Contact(email="malyyigor34@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('tasks', TaskViewSet, basename='task')
router.register('todos', ToDoListViewSet, basename='todos')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', custom_admin_site.urls),
    path('', include(router.urls)),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]
