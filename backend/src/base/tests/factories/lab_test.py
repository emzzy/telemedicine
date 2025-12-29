import factory
from faker import Faker

fake = Faker()

class LabTestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'base.models.LabTest'

    appointment = factory.SubFactory('base.tests.factories.appointment.AppointmentFactory') # pyright: ignore[reportPrivateImportUsage]
    test_name = 'testing lab'
    description = fake.texts()
    result = fake.text()