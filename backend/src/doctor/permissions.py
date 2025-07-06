from rest_framework import permissions

class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        doctor = request.user.is_medical_professional
        return request.user.is_medical_professional or request.user.is_admin