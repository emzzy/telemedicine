from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('user-signup/', views.UserRegistrationView.as_view(), name='api-user-signup'),
    path('user-login/', views.LoginAPIView.as_view(), name='api-user-login'),
    path('user-logout/', views.UserLogoutSerializer, name='api-user-logout'),
    path('verify-email/', views.VerifyEmail.as_view(), name='api-verify-email'),
    path('select-role/', views.SelectedRole.as_view(), name='api-select-role'),
    path('users/', views.ListUsersAPIView.as_view(), name='users'), # returns all users from table
    path('users/get-user/<int:pk>', views.GetUserView.as_view(), name='get-user'), # returns one user with their pk
    path('users/patients/', views.ListPatientView.as_view(), name='is-patient'), # returns only patients from table
    path('users/medical-professionals/', views.ListMedicalProfessionalView.as_view(), name='is-medical-professional'), # returns only med prof from table
    path('users/delete-user/<int:pk>', views.DeleteUserAccount.as_view(), name='delete-user')
]
urlpatterns = format_suffix_patterns(urlpatterns)