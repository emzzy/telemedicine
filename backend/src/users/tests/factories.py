import factory
from faker import Faker

from users.models import UserAccount

fake = Faker()

class UserAccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserAccount
        
    email = factory.Faker('email') # pyright: ignore[reportPrivateImportUsage]
    first_name = factory.Faker('first_name') # type: ignore
    last_name = factory.Faker('last_name') # type: ignore
    password = factory.PostGenerationMethodCall('set_password', 'Password1234') # type: ignore
    phone_number = '07123456789'
    gender = factory.Iterator(['Male', 'Female', 'Other', 'Prefer not to say']) # type: ignore
    date_of_birth = factory.Faker('date_of_birth', minimum_age=18, maximum_age=95) # type: ignore

    is_active = True
    is_admin = False
    is_staff = False
    is_superuser = False
    is_verified = False
    is_patient = False
    is_medical_professional = False