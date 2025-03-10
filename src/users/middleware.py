from http import HTTPStatus
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model


# class UserMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         path = request.path
#         user = request.user

#         if path.startswith('/patients/') and not user.is_patient:
#             response = JsonResponse({'message': 'you are not authorized to access this page'}, status=HTTPStatus.UNAUTHORIZED)
        
#         if path.startswith('/medicals/') and not user.is_medical_professional:
#             response = JsonResponse({'message': 'you are not authorized to access this page'}, status=HTTPStatus.UNAUTHORIZED)

#         if path.startswith('/select-role/') and 'type' in request.GET:
#             role = request.GET.get('type')
#             if role in ['PATIENT', 'MEDICALPROFESSIONAL']:
#                 request.session['select-role'] = role
#                 return redirect(reverse('user-signup/'))

#         response = self.get_response(request)

#         return response

class CustomUserRedirect:
    def __init__(self, get_response):
        self.get_response = get_response
        self.role_dashboard_mapping = {
            'patient': '/patient-dashboard/',
            'medical_professional': '/is_medicalprofessional'
        }

    def __call__(self, request):
        
        if not request.user.is_authenticated:
            return self.get_response(request)
        
        current_path = request.path
        user_role = self.get_user_role(request)

        if current_path in ['/login', '/logout/', '/admin/']:
            print(f'special path access: {current_path}')

        dashboard_url = self.role_dashboard_mapping.get(user_role)
        if dashboard_url and not current_path.startswith(dashboard_url):
            return redirect(dashboard_url)
        
        return self.get_response(request)
    
    def get_user_role(self, request):
        session_role = request.session.get('select-role')
        if session_role:
            return session_role
        
        user = request.user
        
        if hasattr(user, 'patient') and user.is_patient:
            return 'patient'
        elif hasattr(user, 'medical_professional') and user.is_medical_professional:
            return 'medical_professional'

        return None