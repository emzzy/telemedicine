from django.test import TestCase, APIClient
from api.models import Patient, MedicalProfessional
from django.urls import reverse
from rest_framework import status

class PatientViewsTestCase(TestCase):
    def setUp(self):
        # Set up test users and data
        self.client = APIClient()

        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")
        
        # Create some sample Patients and Medical Professionals
        self.patient = Patient.objects.create(first_name="John", last_name="Doe", date_of_birth="2000-01-01")
        self.medical_professional = MedicalProfessional.objects.create(name="Dr. Smith", specialty="Cardiology")

        # Define URLs for testing
        self.patient_url = "/patients/"
        self.medical_professional_url = "/doctors/"

        
    
