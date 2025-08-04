from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        admin_email = settings.ADMIN_USER_EMAIL
        admin_password = settings.ADMIN_USER_PASSWORD
        admin_first_name = settings.ADMIN_USER_FIRSTNAME
        admin_last_name = settings.ADMIN_USER_LASTNAME

        if not admin_email or not admin_password:
            self.stdout.write(
                self.style.ERROR('ADMIN_USER_EMAIL and ADMIN_USER_PASSWORD must be set in environment variables')
            )
            return

        # Check if admin user already exists
        if User.objects.filter(email=admin_email).exists():
            self.stdout.write(
                self.style.WARNING(f'Admin user with email {admin_email} already exists')
            )
            return

        # Create the admin user (email-based user model)
        admin_user = User.objects.create_superuser(
            email=admin_email,
            password=admin_password,
            first_name=admin_first_name,
            last_name=admin_last_name
        )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created admin user: {admin_first_name} ({admin_email})')
        )