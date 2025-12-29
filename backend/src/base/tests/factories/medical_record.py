import factory
from faker import Faker

from base.models import MedicalRecord

fake = Faker()

class MedicalRecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MedicalRecord
    
    appointment = factory.SubFactory('base.tests.factories.appointment.AppointmentFactory') # pyright: ignore[reportPrivateImportUsage]
    diagnosis = fake.texts()
    treatment = fake.texts()