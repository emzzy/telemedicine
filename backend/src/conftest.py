import pytest

from pytest_factoryboy import register
from users.tests.factories import UserAccountFactory
from users.models import UserAccount

register(UserAccountFactory)


# @pytest.fixture
# def create_user(db):
#     user = UserAccount.objects.create(
#         email="test@mail.com",
#         first_name="Doe",
#         last_name="John",
#         password="securepassword",
#         confirm_password="securepassword",
#         phone_number="123456789",
#         gender="male",
#         date_of_birth="1990-01-01",
#         location="City Name",
#         role="medical_professional",
#     )
#     return user

# @pytest.fixture
# def new_user_factory(db):
#     def create_app_user(
#         email: str = "test@mail.com",
#         first_name: str = "Doe",
#         last_name: str = "John",
#         password: str = None,
#         confirm_password: str = "securepassword",
#         phone_number: str = "123456789",
#         gender: str = "male",
#         date_of_birth: str = "1990-01-01",
#         location: str = "City Name",
#         is_active: str = True,
#         is_superuser: str = False,
#         is_staff: str = False,
#     ):
#         user = UserAccount.objects.create_user(
#             email=email,
#             first_name=first_name,
#             last_name=last_name,
#             password=password,
#             is_active=is_active,
#             is_superuser=is_superuser,
#             is_staff=is_staff,
#         )
#         return user
#     return create_app_user


@pytest.fixture
def new_user1(db, user_account_factory):
    user = user_account_factory.create()
    print(UserAccount.objects.all().count())
    return user
