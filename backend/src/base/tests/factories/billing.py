import factory
from faker import Faker

from base.tests.factories.appointment import AppointmentFactory
from patient.tests.factories import PatientFactory
from base.models import Billing

fake = Faker()

class BillingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Billing

    patient = factory.SubFactory(PatientFactory) # pyright: ignore[reportPrivateImportUsage]
    appointment = factory.SubFactory(AppointmentFactory) # pyright: ignore[reportPrivateImportUsage]
    sub_total = fake.pricetag()
    tax = fake.pricetag()
    total = fake.pricetag()
    status = 'status'
    billing_id = '5547896'
