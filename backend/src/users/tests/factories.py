import factory
from faker import Faker

from users.models import UserAccount

fake = Faker()

class UserAccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserAccount
        
    email = fake.email()
    first_name = fake.first_name()
    last_name = fake.last_name()
    password = fake.password()
    is_staff = 'True'