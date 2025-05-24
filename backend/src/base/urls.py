from django.urls import path
from base.views import ServiceDetailView, ServicesListView, CheckoutView, BookAppointment

urlpatterns = [
    path('services/', ServicesListView.as_view(), name='services-list'),
    path('service/<int:pk>', ServiceDetailView.as_view(), name='service-details'),
    path('book-appointment/<int:service_id>/<int:doctor_id>/', BookAppointment.as_view(), name='book_appointment'),
    path('billing/<int:billing_id>/', CheckoutView.as_view(), name='checkout')
]