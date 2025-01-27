from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializer  import UserAccountSerializer, UserRegistrationSerializer, UserLoginSerializer
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from users.models import UserAccount
import logging
from django.contrib import messages

class SelectedRole(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        role = request.POST.get('role')
        
        if role not in ['patient', 'medical_professional']:
            return Response({'error': 'invalid_role'}, status=status.HTTP_400_BAD_REQUEST)
        
        request.session['selected_role'] = role # save the role in a session

        print(f'selected role before signup: {role}') # debuging
        print(f'redirecting to: {reverse('signup')}') # debuging

        return redirect(reverse('signup'))

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        """handles GET request to show role-specific signup data. Redirects to the select-role view if no role is in session"""
        role = request.session.get('selected_role', None) or request.data.get('role')
        if not role:
            return redirect(reverse('select-role'))
        return Response({'message': f'Signing up as: {role}'}, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        """handles POST request to register a user. Attaches the is_patient or is_medical_professional
        flag based on the selected role"""
        role = request.session.get('selected_role', None) or request.data.get('role')
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
            user = UserAccount.objects.get(email=request.data['email'])
            token = Token.objects.create(user=user)
            
            messages.success(request, "Account has been created successfully. Please Login")
            request.session.pop('selected_role', None)

            return Response({"token": token.key, "User": serializer.data}, status=status.HTTP_201_CREATED)
        
        messages.error(request, "There was an error duing registration")

        logging.info(f"Serializer errors: {serializer.errors}")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(email=serializer.data['email'], password=serializer.data['password'])
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': [token.key], 'Success': 'Login successful'}, status=status.HTTP_201_CREATED)
            return Response({'Message': 'Invalid email and password'}, status=status.HTTP_401_UNAUTHORIZED)


# class UserRegistrationView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         """To register new user(s)"""
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             print(request)
#             return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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