from django.urls import path
from . import views
from .views import SelectedRole, ListUsersAPIView, ListMedicalProfessionalView, ListMedicalProfessionalView, UserRegistrationView, GetUserView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('signup/', UserRegistrationView.as_view(), name='user-signup'),
    #
    path('select-role/', SelectedRole.as_view(), name='select-role'),
    path('users/', ListUsersAPIView.as_view(), name='users'), # returns all users from table
    path('users/get-user/<int:pk>', GetUserView.as_view(), name='get-user'), # returns one user with their pk
    path('users/is-patient/', ListMedicalProfessionalView.as_view(), name='is-patient'), # returns only patients from table
    path('users/is-medical-professional/', ListMedicalProfessionalView.as_view(), name='is-medical-professional'), # returns only med prof from table
]
urlpatterns = format_suffix_patterns(urlpatterns)