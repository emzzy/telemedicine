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


class PatientListAPIView(generics.ListCreateAPIView):
    """List all patients, or create new patient"""
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    #permission_classes = [IsAdminUser, IsAuthenticated] # admin, and authenticated can access this view


class PatientDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a patient instance"""
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    

class MedicalProfessionalListAPIView(generics.ListCreateAPIView):
    """List all medical professionals, or create new"""
    queryset = MedicalProfessional.objects.all()
    serializer_class = MedicalProfessionalSerializer
    #permission_classes = [IsAuthenticated]


class MedicalProfessionalDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a patient instance"""
    queryset = MedicalProfessional.objects.all()
    serializer_class = MedicalProfessionalSerializer
    #permission_classes = [IsAuthenticated]
    

class IsDoctorAPIView(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'doctor'


class PatientSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response()
        
        # to check if record exists
        if Patient.objects.filter(email=email).exists():
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        # proceed to create the user if above passes
        return Response({"Message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    

@api_view(['POST'])
def patient_login(request):
    patient = get_object_or_404(Patient, username=request.data['username'])
    if not patient.check_password(request.data['password']):
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    token = Token.objects.get_or_create(patient=patient)
    serializer = PatientSerializer(instance=patient)
    return Response({"token": token.key, "patient": serializer.data})
