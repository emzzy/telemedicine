from .appointment import AppointmentFactory
from .medical_record import MedicalRecordFactory
from .billing import BillingFactory
from .lab_test import LabTestFactory
from .prescription import PrescriptionFactory
from .service import ServiceFactory


__all__ = [
    'AppointmentFactory',
    'MedicalRecordFactory',
    'BillingFactory',
    'LabTestFactory',
    'PrescriptionFactory',
    'ServiceFactory',
]