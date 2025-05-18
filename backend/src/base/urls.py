from django.urls import path
from base import views

urlpatterns = [
    path('services/', views.ServicesListView.as_view(), name='services-list'),
    path('service/<int:pk>', views.ServiceDetailView.as_view(), name='service-details'),
    path('book-appointment/<int:service_id>/<int:doctor_id>/', views.BookAppointment.as_view(), name='book_appointment'),
]