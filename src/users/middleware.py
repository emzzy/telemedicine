from http import HTTPStatus
from django.http import JsonResponse

class PatientMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # one time configuration and initialization

    def __call__(self, request):
        path = request.path
        user = request.user

        if path.startswith('patients/'):
            if not user.is_patient:
                response = JsonResponse({'message': 'you are not authorized to access this page'}, status=HTTPStatus.UNAUTHORIZED)

                return response
        
        if path.startswith('medicals/'):
            if not user.is_medical_professional:
                response = JsonResponse({'message': 'you are not authorized to access this page'}, status=HTTPStatus.UNAUTHORIZED)

                return response
        
        response = self.get_response(request)

        return response
