import factory
from faker import Faker

from base.tests.factories import AppointmentFactory
from doctor.models import MedicalProfessional, Notification
from django.contrib.auth import get_user_model
from users.tests.factories import UserAccountFactory

User = get_user_model()
fake = Faker()

class MedicalProfessionalFactory(factory.django.DjangoModelFactory):
    class Meta:
        models = MedicalProfessional

    user = factory.SubFactory(UserAccountFactory)
    title = fake.name
    image = fake.image()
    image_caption = fake.catch_phrase_verb()
    bio = fake.texts()
    medical_license = fake.license_plate()
    specialty = fake.text()
    years_of_experience = fake.house_number()
    professional_certificate = fake.file_extension()
    available_appointment_date = fake.date_time_ad


class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification

    doctor = factory.Subfactory(MedicalProfessionalFactory)
    appointment = factory.Subfactory(AppointmentFactory)
    type = fake.name()
    seen = fake.boolean()
    date = fake.date_time()