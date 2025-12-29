import factory
from faker import Faker

from base.tests.factories.appointment import AppointmentFactory
from base.models import LabTest

fake = Faker()

class LabTestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LabTest

    appointment = factory.SubFactory(AppointmentFactory) # pyright: ignore[reportPrivateImportUsage]
    test_name = 'testing lab'
    description = fake.texts()
    result = fake.text()
