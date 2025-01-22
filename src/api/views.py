from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializer  import UserAccountSerializer, UserRegistrationSerializer
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from users.models import UserAccount
import logging


class SelectedRole(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        role = request.POST.get('role')
        
        if role not in ['patient', 'medical_professional']:
            return Response({'error': 'invalid_role'}, status=status.HTTP_400_BAD_REQUEST)
        
        request.session['selected_role'] = role # save the role in a session
        print(f'selected role before signup: {role}')
        print(f'redirecting to: {reverse('signup')}')
        return redirect(reverse('signup'))

class SignUpView(APIView):
    """Retrieves the selected role from session, validates input, and creates a user"""
    def get(self, request, *args, **kwargs):
        """handles GET request to show role-specific signup data. Redirects to the select-role view if no role is in session"""
        role = request.session.get('selected_role', None)
        if not role:
            return redirect(reverse('select-role'))
        return Response({'message': f'Signing up as: {role}'}, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        """handles POST request to register a user. Attaches the is_patient or is_medical_professional flag based on the selected role"""
        role = request.session.get('selected_role', None)
        if not role:
            return Response(
                {'error': 'Role not specified. Please select a role first.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        logging.info(f'Selected role before signup: {role}')

        serializer = UserRegistrationSerializer(data=request.data, context={'role': role})

        logging.info(f"Serializer context: {serializer.context}")

        if serializer.is_valid():
            serializer.save()

            # if role == 'patient':
            #     user.is_patient = True
            # elif role == 'medical_professional':
            #     user.is_medical_professional = True
            # user.save()
            print(f'selected role after signup: {role}')
            # clear session
            request.session.pop('selected_role', None)
            return redirect(reverse('user-login'))
        logging.info(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    pass

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