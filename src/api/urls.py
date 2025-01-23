from django.urls import path
from .views import SelectedRole, ListUsersAPIView, ListMedicalProfessionalView, ListMedicalProfessionalView, UserRegistrationView, GetUserView, LoginView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('user-signup/', UserRegistrationView.as_view(), name='api-user-signup'),
    path('login/', LoginView.as_view(), name='api-user-login'),
    path('select-role/', SelectedRole.as_view(), name='api-select-role'),
    path('users/', ListUsersAPIView.as_view(), name='users'), # returns all users from table
    path('users/get-user/<int:pk>', GetUserView.as_view(), name='get-user'), # returns one user with their pk
    path('users/is-patient/', ListMedicalProfessionalView.as_view(), name='is-patient'), # returns only patients from table
    path('users/is-medical-professional/', ListMedicalProfessionalView.as_view(), name='is-medical-professional'), # returns only med prof from table
]
urlpatterns = format_suffix_patterns(urlpatterns)