import pytest
from rest_framework.test import APIClient

client = APIClient()

payload = dict(
        first_name='john',
        last_name='doe',
        email='johndoe@email.com',
        password='securepassword',
        confirm_password='securepassword',
        phone_number='0123456789',
        gender='other',
        date_of_birth='1980-10-03',
        location='Anywhere',
        role='patient'
    )

gagag = 

@pytest.mark.django_db
def test_register_user():
    
    payload = dict(
        first_name='john',
        last_name='doe',
        email='johndoe@email.com',
        password='securepassword',
        confirm_password='securepassword',
        phone_number='0100025452',
        gender='male',
        date_of_birth='1990-01-50',
        location='anywhere',
        role='patient'
    )

    response = client.post('/api/user/signup/', payload)

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


@pytest.mark.django_db
def test_user_login():

    payload = dict(
        first_name='john',
        last_name='doe',
        email='johndoe@email.com',
        password='securepassword',
        confirm_password='securepassword',
        phone_number='0123456789',
        gender='other',
        date_of_birth='1980-10-03',
        location='Anywhere',
        role='patient'
    )

    client.post('/api/user/signup/', payload)

    response = client.post('/api/user/login/', {'email': 'johndoe@email.com', 'password': 'securepassword'}, format='json')
    
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_user_fail():
    response = client.post("/api/user/login/", {'email': "johndoe@email.com", 'password': "securepassword"}, format='json')

    assert response.status_code == 403