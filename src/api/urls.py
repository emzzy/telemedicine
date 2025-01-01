from django.urls import path
from .views import PatientDetails, PatientList, MedProDetails, MedProList
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    #path('user/', get_user, name='get_user'), # one user
    path('patients/', PatientList.as_view(), name='patients-list'), # all patients
    path('patients/<int:pk>', PatientDetails.as_view(), name='patient-details'),
    path('doctors/', MedProList.as_view(), name='doctors-list'),
    path('doctors/<int:pk>', MedProDetails.as_view(), name='doctor-details'),
]
urlpatterns = format_suffix_patterns(urlpatterns)