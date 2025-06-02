from django.urls import path
from base.views import ( ServiceDetailView, ServicesListView, CheckoutView, BookAppointment, 
    CreateStripeCheckoutSession, stripe_verify_payment, paypal_payment_verify
)

urlpatterns = [
    path('services/', ServicesListView.as_view(), name='services-list'),
    path('service/<int:pk>', ServiceDetailView.as_view(), name='service-details'),
    path('book-appointment/<int:service_id>/<int:doctor_id>/', BookAppointment.as_view(), name='book_appointment'),
    path('billing/<int:billing_id>/', CheckoutView.as_view(), name='checkout'),
    path('create-checkout-session/<int:billing_id>/', CreateStripeCheckoutSession.as_view(), name='checkout-session'),
    path('verify-payment/<str:session_id>/', stripe_verify_payment, name='verify-payment'),
    path('paypal/verifypal/<int:billing_id>/', paypal_payment_verify, name='paypal_payment_verify'),
]