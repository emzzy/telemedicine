import pytest

from pytest_factoryboy import register
from django.contrib.auth import get_user_model
from users.models import UserAccount
from patient.models import Patient
from doctor.models import MedicalProfessional


User = get_user_model()

register(UserAccount)


@pytest.fixture
def new_user(db, user_factory):
    user = user_factory.create()
    return user


@pytest.fixture
def user_data():
    return {
        "email": "eazy@gmail.com",
        "first_name": "Doe",
        "last_name": "John",
        "password": "securepassword",
        "confirm_password": "securepassword",
        "phone_number": "123456789",
        "gender": "male",
        "date_of_birth": "1990-01-01",
        "location": "City Name",
        "role": "medical_professional",
    }

@pytest.fixture
def create_user(db, user_data):
    user = user_data.create()
    return UserAccount.objects.create(
        email="eazy@gmail.com",
        first_name="Doe",
        last_name="John"
        password="securepassword",
        
        confirm_password="securepassword",
        phone_number="123456789",
        gender="male",
        date_of_birth="1990-01-01",
        location="City Name",
        role="medical_professional",
    )

@pytest.fixture
def user_patient(db, create_user):
    pass