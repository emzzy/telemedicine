from django.test import TestCase
from api.models import Patient, MedicalProfessional
from django.urls import reverse
from rest_framework import status

class PatientViewsTestCase(TestCase):

    def test_view_patients_unauthenticated(self):
        response = self.client.get(reverse('patients-list'))
        self.assertEqual(response.status_code, 403)
    
    def test_view_patients_unauthenticated(self):
        response = self.client.get(reverse('patients-details'))
        self.assertEqual(response.status_code, 201)    
     