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
from rest_framework_simplejwt.views import TokenRefreshView
from api.views import MyObtainTokenPairView
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    home_view,
    user_register_view,
    user_login,
    role_selector, patient_dashboard, med_pro_dashboard,
)

urlpatterns = [
    path("", home_view, name="home"),
    path('agora/', include('agora.urls')),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('token/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', user_register_view, name='signup'),
    path('login/', user_login, name='login'),
    path('select-role/', role_selector, name='select-role'),
    path('patient-dashboard/', patient_dashboard, name='patient-dashboard'),
    path('medical-professional-dashboard/', med_pro_dashboard, name='medical-professional-dashboard'),
    path('silk/', include('silk.urls', namespace='silk')) # for api optimization during development
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)