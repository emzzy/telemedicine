from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Patient, MedicalProfessional
from .serializer  import PatientSerializer, MedicalProfessionalSerializer
from rest_framework.views import APIView
from django.http import Http404


def get_user(request):
    """get one specific user from db"""
    return Response(PatientSerializer(
        {
            "first_name": "Mustarrrrrdd!!!", 
            "last_name": "GNX", 
        }
    ).data)

class PatientList(APIView):
    """List all patients or create a new patient."""
    def get_all_patients(self, request, format=None):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    def post(request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientDetail(APIView):
    """Retrieve, update, or delete a patient instance."""
    def get_object(self, pk):
        try:
            return Patient.objects.get(pk=pk)
        except Patient.DoesNotExist:
            raise Http404  
    
    def get(self, request, pk, format=None):
        patient = self.object.get(pk)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        patient = self.get_object(pk)
        serializer = PatientSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        patient = self.get_object(pk)
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MedicalProList(APIView):
    """List all Professionals, or create new professional."""
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


class MedicalProDetail(APIView):
    """Retrieve, update, or delete a medical professional instance"""
    def get_objects(self, pk):
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