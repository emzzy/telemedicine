import pytest

from doctor.tests.factories import MedicalProfessionalFactory
from users.tests.factories import UserAccountFactory
from base.models import Service

@pytest.mark.skip
def test_appointment(appointment_factory):
    appointment = appointment_factory.build()
    print(appointment.doctor.user.first_name)
    assert True


@pytest.mark.django_db
@pytest.mark.parametrize(
    'image, name, description, cost',
    [
        ('service_image_url', 'service_name', 'this service offfers solution to treat teeth problems' , 50.0),
    ],
)
def test_service_instance(db, service_factory, image, name, description, cost):
    doctors_list = UserAccountFactory(is_medical_professional=True)
    doctor_description = MedicalProfessionalFactory()

    service = service_factory(
        image=image,
        name=name,
        description=description,
        cost=cost,
        available_doctors=[doctors_list],
        doctor_details=[doctor_description],
    )
    assert Service.objects.all().count() == 1