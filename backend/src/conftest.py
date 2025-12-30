import pytest

from pytest_factoryboy import register
from users.models import UserAccount

from users.tests.factories import UserAccountFactory
register(UserAccountFactory)

from patient.tests.factories import PatientFactory
register(PatientFactory)

from doctor.tests.factories import MedicalProfessionalFactory
register(MedicalProfessionalFactory)

from base.tests.factories import (
    AppointmentFactory, BillingFactory, ServiceFactory, MedicalRecordFactory, LabTestFactory, PrescriptionFactory,
)

register(AppointmentFactory)
register(ServiceFactory)
register(MedicalRecordFactory)
register(LabTestFactory)
register(PrescriptionFactory)
register(BillingFactory)


@pytest.fixture
def new_user1(db, user_account_factory):
    user = user_account_factory.create()
    print(UserAccount.objects.all().count())
    return user

