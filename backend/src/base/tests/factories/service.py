import factory
from faker import Faker

from base.models import Service

fake = Faker()

class ServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Service
    
    image = image = factory.django.ImageField(filename='service.jpg', width=100, height=100, color='red')
    name = factory.Faker('word')
    description = factory.Faker('text')
    cost = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)

    @factory.post_generation # pyright: ignore[reportPrivateImportUsage]
    def available_doctors(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for doctor in extracted:
                self.available_doctors.add(doctor)
        else:
            from users.tests.factories import UserAccountFactory
            doctor = UserAccountFactory(is_medical_professional=True)
            self.available_doctors.add(doctor)
    
    @factory.post_generation # pyright: ignore[reportPrivateImportUsage]
    def doctor_details(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for doctor in extracted:
                self.doctor_details.add(doctor)
        else:
            from doctor.tests.factories import MedicalProfessionalFactory

            doctor = MedicalProfessionalFactory()
            self.doctor_details.add(doctor)