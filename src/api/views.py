from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from .models import Patient, MedicalProfessional
from .serializer  import PatientSerializer, MedicalProfessionalSerializer
from django.http import Http404
from django.contrib.auth.models import User


class PatientListAPIView(generics.ListCreateAPIView):
    """List all patients, or create new patient"""
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated] # admin, and authenticated can access this view


class PatientDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a patient instance"""
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    

class MedicalProfessionalListAPIView(generics.ListCreateAPIView):
    """List all medical professionals, or create new"""
    queryset = MedicalProfessional.objects.all()
    serializer_class = MedicalProfessionalSerializer
    permission_classes = [IsAuthenticated]


    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serializer = MedicalProfessionalSerializer
    #     return Response(serializer.data)
    
    # def get(self, request, format=None):
    #     mp = MedicalProfessional.objects.all()
    #     serializer = MedicalProfessionalSerializer(mp, many=True)
    #     return Response(serializer.data)
    
    # def post(self, request, format=None):
    #     serializer = MedicalProfessionalSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MedicalProfessionalDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a patient instance"""
    queryset = MedicalProfessional.objects.all()
    serializer_class = MedicalProfessionalSerializer
    permission_classes = [IsAuthenticated]
    

class IsDoctorAPIView(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'doctor'
    