from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Patient, MedicalProfessional
from .serializer  import PatientSerializer, MedicalProfessionalSerializer
from django.http import Http404


class PatientList(APIView):
    """List all patients, or create new patient"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user), # django.contrib.auth.user instance
            'auth': str(request.auth), # None
        }
        return Response(content)

    def get(self, request, format=None):
        patient = Patient.objects.all()
        serializer = PatientSerializer(patient, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PatientDetails(APIView):
    """Retrieve, update, or delete a patient instance"""
    def get_object(self, pk):
        try:
            return Patient.objects.get(pk=pk)
        except Patient.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        patient = self.get_object(pk)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        patient = self.get_object(pk)
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        patient = self.get_object(pk)
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class MedProList(APIView):
    """List all medical professionals, or create new"""
    def get(self, request, format=None):
        mp = MedicalProfessional.objects.all()
        serializer = MedicalProfessionalSerializer(mp, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = MedicalProfessionalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MedProDetails(APIView):
    """Retrieve, update, or delete a patient instance"""
    def get_object(self, pk):
        try:
            return MedicalProfessional.objects.get(pk=pk)
        except MedicalProfessional.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        mp = self.get_object(pk)
        serializer = MedicalProfessionalSerializer(mp)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        mp = self.get_object(pk)
        serializer = MedicalProfessionalSerializer(mp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        mp = self.get_object(pk)
        mp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    