import factory
from faker import Faker

fake = Faker()

class MedicalRecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'base.models.MedicalRecord'
    
    appointment = factory.SubFactory('base.tests.factories.appointment.AppointmentFactory') # pyright: ignore[reportPrivateImportUsage]
    diagnosis = fake.texts()
    treatment = fake.texts()