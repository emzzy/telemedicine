import pytest

from base.models import Service

@pytest.mark.skip
def test_appointment(appointment_factory):
    appointment = appointment_factory.build()
    print(appointment.doctor.user.first_name)
    assert True


@pytest.mark.parametrize(
    'image, name, description, cost, available_doctors, doctor_details',
    [
        ('service_image_url', 'service_name', 'this service offfers solution to treat teeth problems' , 50.0, [1], '1'),
        # ('service_image_url', 'service_name', 'fix your tooth', 1, 'dentist'),
    ],
)
def test_service_instance(
    db, service_factory, image, name, description, cost, available_doctors, doctor_details
):
    test = service_factory(
        image=image,
        name=name,
        description=description,
        cost=cost,
        available_doctors=available_doctors,
        doctor_details=doctor_details
    )
    test = Service.objects.all().count()
    assert test == True