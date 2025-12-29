import factory
from faker import Faker

fake = Faker()

class ServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'base.models.Service'
    
    image = fake.image_url()
    name = 'Optometry'
    description = fake.texts()
    cost = fake.pricetag()

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