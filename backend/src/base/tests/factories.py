import factory
from faker import Faker

from doctor.tests.factories import MedicalProfessionalFactory
from patient.tests.factories import PatientFactory
from users.tests.factories import UserAccountFactory
from base import models

fake = Faker()

class ServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Service
    
    image = fake.image_url()
    name = fake.name()
    description = fake.texts()
    cost = fake.pricetag()
    available_doctors = factory.SubFactory(UserAccountFactory)
    doctor_details = factory.SubFactory(MedicalProfessionalFactory)


class AppointmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Appointment

    service = factory.SubFactory(ServiceFactory)
    doctor = factory.SubFactory(MedicalProfessionalFactory)
    patient = factory.SubFactory(PatientFactory)
    appointment_date = fake.date_time()
    issues = fake.text()
    symptoms = fake.text()
    appointment_id = fake.toll_number()
    status = 'status'


class MedicalRecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.MedicalRecord
    
    appointment = factory.SubFactory(AppointmentFactory)
    diagnosis = fake.texts()
    treatment = fake.texts()

class LabTestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.LabTest

    appointment = factory.SubFactory(AppointmentFactory)
    test_name = fake.city_name()
    description = fake.texts()
    result = fake.text()


class PrescriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Prescription

    appointment = factory.SubFactory(AppointmentFactory)
    medication = fake.text()


class BillingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Billing

    patient = factory.SubFactory(PatientFactory)
    appointment = factory.SubFactory(AppointmentFactory)
    sub_total = fake.pricetag()
    tax = fake.pricetag()
    total = fake.pricetag()
    status = 'status'
    billing_id = fake.land_number()
