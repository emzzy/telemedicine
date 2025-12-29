import factory
from faker import Faker

from base.models import Billing

fake = Faker()

class BillingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Billing

    patient = factory.SubFactory('patient.tests.factories.PatientFactory') # pyright: ignore[reportPrivateImportUsage]
    appointment = factory.SubFactory('base.tests.factories.appointment.AppointmentFactory') # pyright: ignore[reportPrivateImportUsage]
    sub_total = fake.pricetag()
    tax = fake.pricetag()
    total = fake.pricetag()
    status = 'status'
    billing_id = '5547896'
