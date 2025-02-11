from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer  import ( UserAccountSerializer, UserRegistrationSerializer, UserLoginSerializer, 
    UserLogoutSerializer, EmailVerificationSerializer)
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from users.models import UserAccount
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from .utils import Util
import logging
import jwt
from decouple import config
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings


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
    
    @swagger_auto_schema(
            operation_description="Register new user",
            request_body=UserRegistrationSerializer,
            responses={201: "User created succesfully", 400: "Validation error"}
    )
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

            token = RefreshToken.for_user(user).access_token

            current_site = get_current_site(request).domain
            relativeLink = reverse('api-verify-email')

            absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
            email_body = 'Hi '+user.first_name+' Use the link below to verify your email\n' + absurl
            data = {'email_body': email_body,
                    'to_email': user.email, 
                    'email_subject': 'Verify your email'
                }
            Util.send_email(data)

            messages.success(request, "Account has been created successfully. Please Login")
            request.session.pop('selected_role', None)

            return Response({"token": str(token), "User": serializer.data}, status=status.HTTP_201_CREATED)
        
        messages.error(request, "There was an error duing registration")

        logging.info(f"Serializer errors: {serializer.errors}")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            user = authenticate(request, email=email, password=password)

            if user:
                if user.is_patient:
                    dashboard_view = '/patient-dashboard/'
                elif user.is_medical_professional:
                    dashboard_view = '/medical-professional-dashboard/'
                else:
                    return Response({'error': "user has not been assigned a role"}, status=status.HTTP_400_BAD_REQUEST)
                
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                logging.info(f'User {user.email} logged in successfully')

                return Response({
                    "message": "Login successful",
                    "token": access_token,
                    "redirect_to": dashboard_view
                }, status=status.HTTP_200_OK)
                
            return Response({'error': 'Invalid login details'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    """Logout view"""
    permission_classes = (permissions.IsAuthenticated)

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class VerifyEmail(APIView):
    """Email verification"""
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = UserAccount.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Link Expired!'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError as identifier:
            return Response({'error': 'Invalid token!'}, status=status.HTTP_400_BAD_REQUEST)


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
        """returns all patients in db"""
        patients = UserAccount.objects.filter(is_patient=True).select_related('patient')
        serializer = UserAccountSerializer(patients, many=True)
        return Response(serializer.data)

class ListMedicalProfessionalView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Returns all medical professsionals in db"""
        is_med_pro = UserAccount.objects.filter(is_medical_professional=True).select_related('medicalprofessional')
        serializer = UserAccountSerializer(is_med_pro, many=True)
        return Response(serializer.data)
    
class DeleteUserAccount(APIView):
    """ Delete user from db"""
    permission_classes = [IsAdminUser, IsAuthenticated]

    def get_object(self, pk):
        try:
            return UserAccount.objects.get(pk=pk)
        except UserAccount.DoesNotExist:
            raise Http404
        
    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
