
from rest_framework import permissions

class IsParent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'parent'

class IsChild(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'child'

class IsOwnerOrParent(permissions.BasePermission):
    """
    Allow child to view only their own data,
    allow parent to access related child data.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'parent':
            return obj.parents.filter(user=request.user).exists()
        elif request.user.role == 'child':
            return obj.user == request.user
        return False
