from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializer  import UserAccountSerializer, UserRegistrationSerializer
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from users.models import UserAccount


class SelectedRole(APIView):
    def post(self, request):
        role = request.data.get('role')
        if role not in ['patient', 'medical_professional']:
            return Response({'error': 'invalid_role'}, status=status.HTTP_400_BAD_REQUEST)
        request.session['role'] = role
        return Response({'message': f'{role} selected successfully'})

class SignUpView(APIView):
    """Retrieves the selected role from session, validates input, and creates a user"""
    def get(self, request, *args, **kwargs):
        """handles GET request to show role-specific signup data. Redirects to the select-role view if no role is in session"""
        role = request.session.get('selected_role', None)
        if not role:
            return redirect('select-role')
        return Response({'message': f'Signing up as: {role}'}, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        """handles POST request to register a user. Attaches the is_patient or is_medical_professional flag based on the selected role"""
        role = request.session.get('selected_role', None)
        if not role:
            return Response(
                {'error': 'Role not specified. Please select a role first.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            if role == 'PATIENT':
                user.is_patient = True
            elif role == 'MEDICALPROFESSIONAL':
                user.is_medical_professional = True
            user.save()
            

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """To register new user(s)"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(request)
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListUsersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return all users in the database"""
        users = UserAccount.objects.all()
        serializer = UserAccountSerializer(users, many=True)
        print(request)
        return Response({'data': serializer.data})

class GetUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Get one user from database"""
        users = get_object_or_404(UserAccount, pk=pk)
        serializer = UserAccountSerializer(users)
        return Response(serializer.data)

class ListPatientView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """returns all patients in database"""
        patients = UserAccount.objects.filter(is_patient=True).select_related('patient')
        serializer = UserAccountSerializer(patients, many=True)
        return Response(serializer.data)

class ListMedicalProfessionalView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Returns all medical professsionals in database"""
        is_med_pro = UserAccount.objects.filter(is_medical_professional=True).select_related('medicalprofessional')
        serializer = UserAccountSerializer(is_med_pro, many=True)
        return Response(serializer.data)