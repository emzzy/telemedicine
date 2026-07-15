import factory
from faker import Faker

from doctor.models import MedicalProfessional, Notification
from users.tests.factories import UserAccountFactory
from django.core.files.uploadedfile import SimpleUploadedFile

fake = Faker()

class MedicalProfessionalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MedicalProfessional

    user = factory.SubFactory(UserAccountFactory) # pyright: ignore[reportPrivateImportUsage]
    title = fake.prefix()
    image = factory.django.ImageField(
        filename='doctor.jpg', width=100, height=100, color='blue'
    )

    image_caption = 'test image caption'
    bio = fake.text(max_nb_chars=200)
    
    medical_license = '7854123652'

    specialty = 'doctor'
    years_of_experience = 5
    
    professional_certificate = factory.django.FileField(
        filename='certificate.pdf', data=b'fake certificate content'
    )
    
    available_appointment_date = None


class DoctorNotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification

    doctor = factory.SubFactory(MedicalProfessionalFactory) # pyright: ignore[reportPrivateImportUsage]

    @factory.lazy_attribute # pyright: ignore[reportPrivateImportUsage]
    def appointment(self):
        from base.tests.factories import AppointmentFactory
        return AppointmentFactory()
    
    type = factory.Faker('word')
    seen = factory.Faker('boolean')
    date = factory.Faker('date_time')