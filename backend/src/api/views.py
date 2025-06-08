from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from api.serializer  import (
    UserRegistrationSerializer, UserLoginSerializer, EmailVerificationSerializer, UserLogoutSerializer, 
    RequestPasswordResetEmailSerializer, SetNewPasswordSerializer, ListDoctorsSerializer, DoctorProfileSerializer
    )
from shared.serializers import UserAccountSerializer
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from users.models import UserAccount
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from .utils import Util
import logging
import jwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings
from .renderers import UserRenderers
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from .utils import Util
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt


class SelectedRole(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        role = request.POST.get('role')
        
        if role not in ['patient', 'medical_professional']:
            return Response({'error': 'invalid_role'}, status=status.HTTP_400_BAD_REQUEST)
        request.session['selected_role'] = role # save the role in a session

        return redirect(reverse('signup'))

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = (UserRenderers,)
    
    def get(self, request, *args, **kwargs):
        """handles GET request to show role-specific signup data. Redirects to the select-role view if no role is in session"""
        role = request.session.get('userRole', None) or request.data.get('role')
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
        role = request.session.get('userRole', None) or request.data.get('role')
        if not role:
            return Response(
                {'error': 'Role not specified. Please select a role first.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserRegistrationSerializer(data=request.data, context={'role': role})

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
            #request.session.pop('selected_role', None)

            return Response({"token": str(token), "User": serializer.data}, status=status.HTTP_201_CREATED)
        
        messages.error(request, "There was an error during registration")

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        operation_description="User login"
    )
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response({'error': 'Invalid login details'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Debugging print statements
        print(f"Authenticated User: {user}")
        print(f"User is_patient: {user.is_patient}")
        print(f"User is_medical_professional: {user.is_medical_professional}")

        if user.is_patient:
            dashboard_url = reverse('home')
        elif user.is_medical_professional:
            dashboard_url = reverse('home')
        else:
            return Response({'error': 'user has not ben assigned a valid role'}, status=status.HTTP_403_FORBIDDEN)
        # update last_login timestamp in the db, create a session
        user.last_login = now()
        user.save(update_fields=['last_login'])
        login(request, user)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        return Response({
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "redirect_to": dashboard_url
        }, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    """Logout view"""
    serializer_class = UserLogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="JWT Access Token. Format: Bearer <token>",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description="Refresh token to be blacklisted")
            },
            required=['refresh_token']
        ),
        responses={
            205: "Logged out successfully",
            400: "Bad Request (Invalid token)",
        }
    )
    @csrf_exempt
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


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


class RequestPasswordResetEmail(generics.GenericAPIView):
    """password reset request via email"""
    permission_classes = [permissions.AllowAny]
    serializer_class = RequestPasswordResetEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = request.data.get('email', '')

        try: # checks if the email user exists
            user = UserAccount.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))

        except UserAccount.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # generate a password reset token and encodes the user id
        token = PasswordResetTokenGenerator().make_token(user) #changes assigned token after password reset to prevent reuse by another user
        
        #current_site = get_current_site(request=request).domain # parsed request as data from UserRegistraation view
        relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token}) # generate url path to password reset confirmation page
        redirect_url = request.data.get('redirect_url', '')

        absurl = request.build_absolute_uri(relativeLink) # convert the relative path to full url
        
        email_body = f'Hello {user.first_name},\nUse the link below to reset your password. \n{absurl}?redirect_url={redirect_url}'
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Reset your password'
        }
        Util.send_email(data)

        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    """This view takes user request and validates the password reset token"""
    serializer_class = SetNewPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = UserAccount.objects.get(id=id)
            
            # check if user does not reuse reset link more than once
            if not PasswordResetTokenGenerator().check_token(user, token):
                if redirect_url and len(redirect_url) > 3: # check if redirect url is present
                    return redirect(f'{redirect_url}?token_valid=False')
                return redirect( '/?token_valid=False')
            
            # if token is valid, redirect to url with 
            if redirect_url and len(redirect_url) > 3:
                return redirect(
                    redirect_url+ f'?token_valid=True&message=Credentials Valid&uidb64={uidb64}&token={token}'
                )
            
            return redirect(f'/?token_valid=True&message=Credentials Valid&uidb64={uidb64}&token={token}')

        except DjangoUnicodeDecodeError:
            if redirect_url:
                return redirect(f'{redirect_url}?token_valid=False')
            return Response(
                {'error': 'Token is invalid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST
            )

            # try:
            #     if not PasswordResetTokenGenerator().check_token(user):
            #         return CustomRedirect(redirect_url+'?token_valid=False')
            
            # except UnboundLocalError as e:
            #     return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPassword(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'Success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class ListUsersAPIView(generics.ListCreateAPIView):
    """Display list of users in db"""
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        security=[{'Bearer': []}],    
        responses={200: "Success", 401: "Unauthorized"}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class GetUserView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        security=[{'Bearer': []}],
        responses={200: "Success", 401: "Unauthorized"}
    )
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
    permission_classes = [AllowAny]

    def get(self, request):
        """Returns all medical professsionals in db"""
        queryset = UserAccount.objects.filter(is_medical_professional=True).select_related('medicalprofessional')
        serializer = DoctorProfileSerializer(queryset, many=True)
        return Response(serializer.data)


class ListDoctorsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """Returns list of doctors with selected fields"""
        from doctor.models import MedicalProfessional
        doctors = MedicalProfessional.objects.select_related('user').all()
        serializer = ListDoctorsSerializer(doctors, many=True)
        return Response(serializer.data)


class DeleteUserAccount(APIView):
    """ Delete user from db"""
    #permission_classes = [IsAdminUser, IsAuthenticated]

    def get_object(self, pk):
        try:
            return UserAccount.objects.get(pk=pk)
        except UserAccount.DoesNotExist:
            raise Http404
        
    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)