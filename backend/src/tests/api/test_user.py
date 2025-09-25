import pytest
from rest_framework.test import APIClient

client = APIClient()

@pytest.mark.django_db
def test_register_user():
    
    payload = dict(
        first_name='john',
        last_name='doe',
        email='johndoe@email.com',
        password='securepassword',
        phone_number='phone_number',
        gender='gender',
        date_of_birth='date_of_birth',
        location='location',
        role='patient'

    )

    response = client.post('/api/user/signup/', payload)

    print(f'status code: {response.status_code}')
    print(f'status code: {response.data}')
    data = response.data

    assert data['email'] == payload['email']
    assert data['first_name'] == payload['first_name']
    assert data['last_name'] == payload['last_name']
    assert data['role'] == payload['role']
    assert data['phone_number'] == payload['phone_number']
    assert data['gender'] == payload['gender']
    assert data['date_of_birth'] == payload['date_of_birth']
    assert data['location'] == payload['location']
    #assert 'password' not in data