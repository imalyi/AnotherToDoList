from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # In accordance with the task requirements, "Ensure that the API is properly authenticated,
        # and only authenticated users can perform write operations (create, update, delete),"
        # every authenticated user can read the entire list of tasks
        if request.method in permissions.SAFE_METHODS:
            return True
        # but editing, updating, and deleting are allowed only for authenticated users.
        return obj.owner == request.user
