from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status, mixins, generics
from rest_framework.response import Response
from .models import Patient, MedicalProfessional
from .serializer  import PatientSerializer, MedicalProfessionalSerializer
from rest_framework.views import APIView
from django.http import Http404


class PatientList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """List all patients or create a new patient."""
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PatientDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    """Retrieve, update, or delete a patient instance."""
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class MedicalProList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """List all Professionals, or create new professional."""
    queryset = MedicalProfessional.objects.all()
    serializer_class = MedicalProfessionalSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MedicalProDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    """Retrieve, update, or delete a medical professional instance"""
    queryset = MedicalProfessional.objects.all()
    serializer_class = MedicalProfessionalSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
