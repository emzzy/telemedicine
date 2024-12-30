from django.urls import path
from .views import PatientDetail, PatientList, MedicalProList, MedicalProDetail
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    #path('user/', get_user, name='get_user'), # one user
    path('patients/', PatientList.as_view(), name='patients'), # all patients
    path('patients/<int:pk>', PatientDetail.as_view(), name='patient-details'),
    path('doctors/', MedicalProList.as_view(), name='get-all-doctors'),
    path('doctors/<int:pk>', MedicalProDetail.as_view(), name='doctor-details')
]