from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
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

    # authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated]

    
class PatientDetailsAPIView(generics.RetrieveAPIView):
    """Retrieve, update, or delete a patient instance"""
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    

class MedicalProfessionalListAPIView(generics.ListAPIView):
    """List all medical professionals, or create new"""
    queryset = MedicalProfessional.objects.all()
    serializer_class = MedicalProfessionalSerializer

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

class MedicalProfessionalDetailsAPIView(generics.RetrieveAPIView):
    """Retrieve, update, or delete a patient instance"""
    queryset = MedicalProfessional.objects.all()
    serializer_class = MedicalProfessionalSerializer
    