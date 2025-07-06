from rest_framework import permissions


class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.patient or request.user.is_admin