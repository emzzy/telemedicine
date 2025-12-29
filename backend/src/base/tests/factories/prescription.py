import factory
from faker import Faker
fake = Faker()

class PrescriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'base.models.Prescription'

    appointment = factory.SubFactory('base.tests.factories.appointment.AppointmentFactory') # pyright: ignore[reportPrivateImportUsage]
    medication = fake.text()