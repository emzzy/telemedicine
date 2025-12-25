import pytest

from pytest_factoryboy import register
from django.contrib.auth import get_user_model
from users.models import UserAccount
from patient.models import Patient
from doctor.models import MedicalProfessional


User = get_user_model()

#register(UserAccount)


# @pytest.fixture
# def new_user(db, user_factory):
#     user = user_factory.create()
#     return user


# @pytest.fixture
# def user_data():
#     return {
#         "email": "eazy@gmail.com",
#         "first_name": "Doe",
#         "last_name": "John",
#         "password": "securepassword",
#         "confirm_password": "securepassword",
#         "phone_number": "123456789",
#         "gender": "male",
#         "date_of_birth": "1990-01-01",
#         "location": "City Name",
#         "role": "medical_professional",
#     }

@pytest.fixture
def create_user(db):
    user = UserAccount.objects.create(
        email="test@mail.com",
        first_name="Doe",
        last_name="John",
        password="securepassword",
        confirm_password="securepassword",
        phone_number="123456789",
        gender="male",
        date_of_birth="1990-01-01",
        location="City Name",
        role="medical_professional",
    )
    return user

@pytest.fixture
def new_user_factory(db, create_user):
    def create_app_user(
        email: str = "test@mail.com",
        first_name: str = "Doe",
        last_name: str = "John",
        password: str = None,
        confirm_password: str = "securepassword",
        phone_number: str = "123456789",
        gender: str = "male",
        date_of_birth: str = "1990-01-01",
        location: str = "City Name",
        role: str = "medical_professional",
        is_active: str = True,
        is_superuser: str = False,
        is_staff: str = False,
    )
    return create_patient_user

@pytest.fixture
def user_A(db, new_user_factory)
    