from rest_framework import permissions


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return ((request.user.is_authenticated
                and (request.user.role == request.user.is_staff))
                or request.user.is_superuser)
