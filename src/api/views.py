from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from .serializer  import UserAccountSerializer, PatientSerializer
from profiles.models import Patient
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404
from users.models import UserAccount


class SelectedRole(APIView):
    def post(self, request):
        role = request.data.get('role')
        if role not in ['patient', 'medical_professional']:
            return Response({'error': 'invalid_role'}, status=status.HTTP_400_BAD_REQUEST)
        request.session['role'] = role
        return Response({'message': f'{role} selected successfully'})

class UserSignupView(APIView):
    pass

@api_view(['POST'])
@permission_classes([AllowAny])
def user_signup(request):
    serializer = PatientSerializer(data=request.data)
    if serializer.is_valid():
        patient = serializer.save()
        patient = Patient.objects.get(username=request.data['username'])
        patient.make_password(request.data['password']) # encrypts the password
        patient.save()
        token = Token.objects.create(patient=patient)
        return Response({"token": token.key, "patient": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print(request.data)
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET'])
def list_users(request):
    """Return all users in the database"""
    users = UserAccount.objects.all()
    serializer = UserAccountSerializer(users, many=True)
    return Response({'data': serializer.data})

@csrf_exempt
@api_view(['GET'])
def get_user(request, pk):
    """Get one user from database"""
    users = get_object_or_404(UserAccount, pk=pk)
    serializer = UserAccountSerializer(users)
    return Response(serializer.data)

class IsPatientView(APIView):
    def get(self, request):
        """returns all patients in database"""
        patients = UserAccount.objects.filter(is_patient=True).select_related('patient')
        serializer = UserAccountSerializer(patients, many=True)
        return Response(serializer.data)

class IsMedicalProfessional(APIView):
    def get(self, request):
        """Returns all medical professsionals in database"""
        is_med_pro = UserAccount.objects.filter(is_medical_professional=True).select_related('medicalprofessional')
        serializer = UserAccountSerializer(is_med_pro, many=True)
        return Response(serializer.data)
    