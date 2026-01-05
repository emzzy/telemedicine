import pytest
from rest_framework.test import APIClient

client = APIClient()

@pytest.mark.django_db
def test_user_signup(client, faker):
    password = faker.password()
    
    payload = {
        'email': faker.email(),
        'first_name': faker.first_name(),
        'last_name': faker.last_name(),
        'password': password,
        'confirm_password': password,
        'phone_number': '123456789',
        'gender': 'male',
        'date_of_birth': faker.date_of_birth(minimum_age=18, maximum_age=90),
        'location': faker.city(),
        'role': 'medical_professional',
    }    
    response = client.post('/api/user/signup/', payload, format='json')
    # print(response.status_code)
    # print(response.json())

    assert response.status_code == 201
    assert password not in response


@pytest.mark.django_db
def test_user_authentication_components(client):
    from django.contrib.auth import authenticate
    from users.models import UserAccount
    
    # create user
    user = UserAccount.objects.create_user(
        email='test@example.com',
        first_name='Test',
        last_name='User',
        password='password1234',
        is_patient=True,
        is_active=True
    )
    
    # Test 2: check password
    assert user.check_password('password1234')
    
    # test authenticate function
    auth_user = authenticate(email='test@example.com', password='password1234')
    assert auth_user is not None

    from api.serializer import UserLoginSerializer
    serializer = UserLoginSerializer(data={
        'email': 'test@example.com',
        'password': 'password1234'
    })
    assert serializer.is_valid(), f"Serializer validation failed: {serializer.errors}"
    
    # test API endpoint
    payload = {
        'email': 'test@example.com',
        'password': 'password1234',
    }
    response = client.post('/api/user/login/', payload, content_type='application/json')

    assert response.status_code == 200