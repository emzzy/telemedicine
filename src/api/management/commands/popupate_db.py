import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum
from users.models import UserAccount

class Command(BaseCommand):
    help = 'Creates app data'

    def handle(self, *args, **kwargs):
        # get or create superuser
        user = UserAccount.objects.filter(email='em@gmail.com').first()
        if not user:
            user = UserAccount.objects.create_superuser(email='em@gmail.com', password='lennovo2024')

        # create patients - email, first_name, last_name, phone_number, gender, date_of_birth, location
        patients = [
            UserAccount(email='dummy@gmail.com', first_name='dummy1', last_name='dummyLast', phone_number='075142568', gender='male')
        ]
