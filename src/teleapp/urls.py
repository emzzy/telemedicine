"""
URL configuration for teleapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    home_view, 
    user_only_view,
    staff_only_view,
    doctor_register_view,
    patient_register_view
)

urlpatterns = [
    path("", home_view, name="home"), # index page -> root page
    path('api/', include('api.urls')),
    path('doctor-signup/', doctor_register_view, name='doctor_signup'),
    path('patient-signup/', patient_register_view, name='patient_signup'),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('silk/', include('silk.urls', namespace='silk')), # for api optimization during development
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
