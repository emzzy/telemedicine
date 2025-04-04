from django.contrib.auth.models import BaseUserManager
from users.models import UserAccount

class MedicalProfessionalManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=UserAccount.Role.MEDICALPROFESSIONAL)
