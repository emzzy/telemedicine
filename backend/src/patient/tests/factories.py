import factory
from faker import Faker

from base.tests.factories import AppointmentFactory
from users.tests.factories import UserAccountFactory
from patient.models import Notification, Patient

fake = Faker()

class PatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Patient

    user = factory.SubFactory(UserAccountFactory)
    image = fake.image()
    image_caption = fake.catch_phrase()
    age = fake.date_of_birth()
    emergency_contact = fake.mobile_number()
    medical_information = fake.texts()
    blood_group = fake.vehicle_category_letter()


class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification

    patient = factory.Subfactory(PatientFactory)
    appointment = factory.Subfactory(AppointmentFactory)
    type = fake.name()
    seen = fake.boolean()
    date = fake.date_time()