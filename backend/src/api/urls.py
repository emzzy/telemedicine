from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from base.views import service_detail
#from  rest_framework.routers import DefaultRouter
# from doctor.views import views as doctor_views
# from patient.views import views as patient_views

# router = DefaultRouter()
# router.register(r'doctor', doctor_views)
# router.register(r'patient', patient_views)

urlpatterns = [
    # Auth views
    path('user-signup/', views.UserRegistrationView.as_view(), name='api-user-signup'),
    path('user-login/', views.LoginAPIView.as_view(), name='api-user-login'),
    path('user-logout/', views.LogoutAPIView.as_view(), name='api-user-logout'),
    path('verify-email/', views.VerifyEmail.as_view(), name='api-verify-email'),
    path('request-reset-email/', views.RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/', views.PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', views.SetNewPassword.as_view(), name='password-reset-complete'),
    path('select-role/', views.SelectedRole.as_view(), name='api-select-role'),
    
    # All Users
    path('users/', views.ListUsersAPIView.as_view(), name='users'), # returns all users from table
    path('users/get-user/<int:pk>', views.GetUserView.as_view(), name='get-user'), # returns one user with their pk
    path('users/patients/', views.ListPatientView.as_view(), name='is-patient'), # returns only patients from table
    path('users/medical-professionals/', views.ListMedicalProfessionalView.as_view(), name='is-medical-professional'), # returns only med prof from table
    path('users/delete-user/<int:pk>', views.DeleteUserAccount.as_view(), name='delete-user'),

    # Patients
    
    # Doctors

    # Services
    #path('service/add-service/', name='add-a-service'),
    path('service/<service_id>/', service_detail, name='service_detail') 
]
urlpatterns = format_suffix_patterns(urlpatterns)