from django.test import TestCase
from api.models import Patient, MedicalProfessional
from django.urls import reverse
from rest_framework import status

class PatientViewsTestCase(TestCase):
    def setUp(self):
        self.patient1 = Patient.objects.create(first_name='chidera', last_name='Ezeh')
        self.patient2 = Patient.objects.create(first_name='ebere', last_name='Chinyelugo')
        self.list_url = reverse('patients-list')

    def test_view_patients_unauthenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # def test_view_get_patients_unauthenticated(self):
    #     response = self.client.get(reverse('patient-details'))
    #     self.assertEqual(response.status_code, 201)

class MedicalProfessionalViewsTestCase(TestCase):

    def setUp(self):
        self.doctor1 = MedicalProfessional.objects.create(first_name='engremma', last_name='Ezeh')
        self.doctor2 = MedicalProfessional.objects.create(first_name='dera', last_name='Nuel')
        self.list_url = reverse('doctors-list')
        
    
    def get_doctors_test(self):     
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['first_name'], self.doctor1.first_name)

    def test_create_doctor(self):
        pass
