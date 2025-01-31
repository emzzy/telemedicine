from http import HTTPStatus
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse

class UserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # one time configuration and initialization

    def __call__(self, request):
        path = request.path
        user = request.user

        if path.startswith('patients/') and not user.is_patient:
            response = JsonResponse({'message': 'you are not authorized to access this page'}, status=HTTPStatus.UNAUTHORIZED)
        
        if path.startswith('medicals/') and not user.is_medical_professional:
            response = JsonResponse({'message': 'you are not authorized to access this page'}, status=HTTPStatus.UNAUTHORIZED)

        if path.startswith('/select-role/') and 'type' in request.GET:
            role_type = request.GET.get('type')
            if role_type in ['PATIENT', 'MEDICALPROFESSIONAL']:
                request.session['select-role'] = role_type
                return redirect(reverse('user-signup/'))

        response = self.get_response(request)

        return response
