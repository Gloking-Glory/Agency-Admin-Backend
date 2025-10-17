from rest_framework.permissions import BasePermission

class IsAdminUserRole(BasePermission):
    """Allows access only to users with role is ADMIN"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'ADMIN')

class IsAgencyUserRole(BasePermission):
    """Allows access only to users with role is AGENCY"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'AGENCY')
