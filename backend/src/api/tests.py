from django.test import TestCase, Client
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import UserAccount

class UserRegistrationTestCase(APITestCase):

    def setup(self):
        self.client = Client()

    def test_user_register_with_role_attached(self):
        session = self.client.session
        session['selected_role'] = 'patient'
        session.save()

        data = {
            "email": "usersz@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "securepassword",
            "confirm_password": "securepassword",
            "phone_number": "123456789",
            "gender": "male",
            "date_of_birth": "1990-01-01",
            "location": "City Name",
            # "is_patient": True,
            # "is_medical_professional": False,
        }
        response = self.client.post('/api/user-signup/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(UserAccount.objects.filter(email="usersz@example.com").exists())

# class PatientViewsTestCase(TestCase):
#     def setUp(self):
#         # Set up test users and data
#         self.client = APIClient()

#         # Create a test user
#         self.user = Patient.objects.create_user(username="testuser", password="testpass")
        
#         # Create some sample Patients and Medical Professionals
#         self.patient = Patient.objects.create(first_name="John", last_name="Doe", date_of_birth="2000-01-01")
#         self.medical_professional = MedicalProfessional.objects.create(name="Dr. Smith", specialty="Cardiology")

#         # Define URLs for testing
#         self.patient_url = "/patients/"
#         self.medical_professional_url = "/doctors/"


