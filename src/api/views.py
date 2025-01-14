from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission, AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from .models import Patient, MedicalProfessional
from .serializer  import PatientSerializer, MedicalProfessionalSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password

class SelectedRole(APIView):
    def post(self, request):
        role = request.data.get('role')
        if role not in ['patient', 'medical_professional']:
            return Response({'error': 'invalid_role'}, status=status.HTTP_400_BAD_REQUEST)
        request.session['role'] = role
        return Response({'message': f'{role} selected successfully'})


class RegisterView(APIView):
    pass

@api_view(['POST'])
@permission_classes([AllowAny])
def signup_patient(request):
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
