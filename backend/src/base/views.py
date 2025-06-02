import requests
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
import stripe.error
import stripe.webhook
from doctor import models as doctor_model
from patient import models as patient_model
from base import models as base_models
from users import models as user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from base.serializers import ServicesListSerializer, BookAppointmentSerializer, BillingSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from decimal import Decimal
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import stripe



User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY


class ServicesListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """Returns list of all available services"""
        services = base_models.Service.objects.all()
        serializer = ServicesListSerializer(services, many=True)
        
        return Response(serializer.data)

class ServiceDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        service = get_object_or_404(base_models.Service, pk=pk)
        #service = base_models.Service.objects.get(id=service_id)
        serializer = ServicesListSerializer(service)
        return Response(serializer.data)


class BookAppointment(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, service_id, doctor_id):
        user_doctor = get_object_or_404(user_model.UserAccount, id=doctor_id)
        service = get_object_or_404(base_models.Service, id=service_id)
        doctor = get_object_or_404(doctor_model.MedicalProfessional, user=user_doctor)
        # get patient
        user_patient = request.user
        patient = get_object_or_404(patient_model.Patient, user=user_patient)
        
        update_patient_data = [
            'first_name', 'last_name', 'email', 'phone_number', 'gender', 'date_of_birth', 'location'
        ]
        for field in update_patient_data:
            if field in request.data:
                setattr(user_patient, field, request.data[field])
        user_patient.save()

        # Update patient information if provided
        if 'gender' in request.data:
            patient.gender = request.data['gender']
        if 'location' in request.data:
            patient.location = request.data['location']
        if 'date_of_birth' in request.data:
            patient.date_of_birth = request.data['date_of_birth']
        patient.save()

        # Create appointment data
        appointment_data = {
            'service': service.id,
            'doctor': doctor.id,
            'patient': patient.id,
            'appointment_date': doctor.available_appointment_date,
            'issues': request.data.get('issues', ''),
            'symptoms': request.data.get('symptoms', ''),
            'status': 'Scheduled'
        }

        serializer = BookAppointmentSerializer(data=appointment_data)
        if serializer.is_valid():
            appointment = serializer.save()
            
            # Billing object
            billing = base_models.Billing.objects.create(
                patient=patient,
                appointment=appointment,
                sub_total=service.cost,
                tax=round(service.cost * Decimal('0.20'), 2),
                total=round(service.cost * Decimal('1.20'), 2),
                status='Unpaid'
            )
            print(request.data)
            return Response({
                'data': serializer.data,
                'appointment': serializer.data,
                'billing_id': billing.billing_id,
                'message': 'Appointment scheduled successfully!'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, billing_id):
        billing = get_object_or_404(base_models.Billing, billing_id=billing_id)
        serializer = BillingSerializer(billing)
        
        return Response({
            'data': serializer.data,
            'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY,
            "paypal_client_id": settings.PAYPAL_CLIENT_ID
        }, status=status.HTTP_200_OK)


class CreateStripeCheckoutSession(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, billing_id, *args, **kwargs):
        billing = get_object_or_404(base_models.Billing, billing_id=billing_id)

        try:
            checkout_session = stripe.checkout.Session.create(
                customer_email=billing.patient.user.email,
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'gbp',
                        'product_data': {
                            'name': f'Appointment with Dr.{billing.appointment.doctor.user.first_name} for {billing.patient.user.first_name}',
                        },
                        'unit_amount': int(billing.total * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                metadata={
                    'billing_id': billing.billing_id,
                },
                success_url=f'{settings.SITE_URL}/payment-success?session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url=f'{settings.SITE_URL}/payment-cancelled',
            )
            return Response({'url': checkout_session.url})
        
        except Exception as e:
            return Response({
                'message': 'something went wrong when creating stripe session',
                'error': str(e)
            }, status=500)

@csrf_exempt
def stripe_verify_payment(request, session_id):
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        billing_id = session['metadata'].get('billing_id')
        billing = base_models.Billing.objects.get(billing_id=billing_id)        
        
        if session.payment_status == 'paid':
            if billing.status == 'Unpaid':
                billing.status = 'Paid'
                billing.save()
                billing.appointment.status = 'Completed'
                billing.appointment.save()

                #notify doctor and patient on completion
                doctor_model.Notification.objects.create(
                    doctor=billing.appointment.doctor,
                    appointment=billing.appointment,
                    type='New Appointment'
                )
                patient_model.Notification.objects.create(
                    patient=billing.appointment.patient,
                    appointment=billing.appointment,
                    type='Appointment Scheduled'
                )
            return JsonResponse({'status': 'success', 'message': 'Payment verified!'})
        
        return JsonResponse({'status': 'unpaid', 'message': 'Payment not completed'})
    except base_models.Billing.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Billing record not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def get_paypal_access_token():
    token_url = 'https://api.sandbox.paypal.com/v1/oauth2/token'
    data = {'grant_type': 'client_credentials'}
    auth = (settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET_KEY)

    response = requests.post(token_url, data=data, auth=auth)

    if response.status_code == 200:
        print('Access Token: ', response.json()['access_token'])
        return response.json()['access_token']
    else:
        raise Exception(f'Failed to get access token from Paypal. Status code: {response.status_code}')


def paypal_payment_verify(request, billing_id):
    transaction_id = request.GET.get('transaction_id')
    if not transaction_id:
        return JsonResponse({'error': 'Transaction ID is required'}, status=400)
    
    try:
        billing = base_models.Billing.objects.get(billing_id=billing_id)
    except base_models.Billing.DoesNotExist:
        return JsonResponse({'error': 'Billing not found'}, status=404)
    
    try:
        access_token = get_paypal_access_token
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    paypal_api_url = f'https://api-m.sandbox.paypal.com/v2/checkout/orders/{transaction_id}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(paypal_api_url, headers=headers)

    if response.status_code == 200:
        paypal_order_data = response.json()
        paypal_payment_status = paypal_order_data.get('status')

        if paypal_payment_status == 'COMPLETED':
            if billing.status == 'Unpaid':
                billing.status = 'Paid'
                billing.save()
                billing.appointment.status = 'Completed'
                billing.appointment.save()

                #notify doctor and patient on completion
                doctor_model.Notification.objects.create(
                    doctor=billing.appointment.doctor,
                    appointment=billing.appointment,
                    type='New Appointment'
                )
                patient_model.Notification.objects.create(
                    patient=billing.appointment.patient,
                    appointment=billing.appointment,
                    type='Appointment Scheduled'
                )
            return JsonResponse({'status': 'success', 'message': 'Payment verified!'})
        else:
            return JsonResponse({'status': 'failure', 'message': 'Payment not completed!'}, status=400)
    else:
        return JsonResponse({'error': 'Failure to verify payment with Paypal!'}, status=500)
