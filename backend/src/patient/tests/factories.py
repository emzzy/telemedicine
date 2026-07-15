import factory
from faker import Faker

from patient.models import Notification, Patient

fake = Faker()

class PatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Patient

    user = factory.SubFactory('users.tests.factories.UserAccountFactory') # pyright: ignore[reportPrivateImportUsage]
    image = fake.image()
    image_caption = fake.catch_phrase()
    age = fake.date_of_birth()
    emergency_contact = '123456789'
    medical_information = fake.texts()
    blood_group = 'AA'


class PatientNotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification

    patient = factory.SubFactory(PatientFactory) # pyright: ignore[reportPrivateImportUsage]

    @factory.lazy_attribute # pyright: ignore[reportPrivateImportUsage]
    def appointment(self):
        from base.tests.factories import AppointmentFactory
        return AppointmentFactory()
    
    # appointment = factory.SubFactory(AppointmentFactory) # pyright: ignore[reportPrivateImportUsage]
    type = fake.name()
    seen = fake.boolean()
    date = fake.date_time()