import factory
from faker import Faker

from base.models import Appointment

fake = Faker()

class AppointmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Appointment

    service = factory.SubFactory('base.tests.factories.service.ServiceFactory') # pyright: ignore[reportPrivateImportUsage]
    doctor = factory.SubFactory('doctor.tests.factories.MedicalProfessionalFactory') # pyright: ignore[reportPrivateImportUsage]
    patient = factory.SubFactory('patient.tests.factories.PatientFactory') # pyright: ignore[reportPrivateImportUsage]
    appointment_date = fake.date_time()
    issues = fake.text()
    symptoms = fake.text()
    appointment_id = '5'
    status = 'status'
