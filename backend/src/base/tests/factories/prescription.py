import factory
from faker import Faker

from base.tests.factories.appointment import AppointmentFactory
from base.models import Prescription

fake = Faker()

class PrescriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Prescription

    appointment = factory.SubFactory(AppointmentFactory) # pyright: ignore[reportPrivateImportUsage]
    medication = fake.text()
