from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Patient, MedicalProfessional
from .serializer  import PatientSerializer, MedicalProfessionalSerializer


@api_view(['GET'])
def get_user(request):
    """get one specific user from db"""
    return Response(PatientSerializer(
        {
            "first_name": "Mustarrrrrdd!!!", 
            "last_name": "GNX", 
        }
    ).data)

@api_view(['GET'])
def get_all_users(request):
    """get all users from db"""
    patients = Patient.objects.all()
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_user(request):
    serializer = PatientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
