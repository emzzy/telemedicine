import pytest


from pytest_factoryboy import register

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
    user = user_account_factory.create(is_patient=True, is_active=True)
    return user

@pytest.fixture(scope='session')
def django_db_setup():
    from django.conf import settings

    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgres',
        'HOST': 'localhost',
        'NAME': 'postgres'
    }

