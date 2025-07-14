from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenBlacklistView
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view, user_register_view, user_login, role_selector, patient_dashboard, med_pro_dashboard, user_logout, service_detail

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Teleapp API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.nuecare.com/policies/terms/",
      contact=openapi.Contact(email="contact@teleapp.local"),
      license=openapi.License(name="Telemedicine License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path("", home_view, name="home"),
   path('service/<service_id>/', service_detail, name='service_detail'),
   path('agora/', include('agora.urls')),
   path('base/', include('base.urls')),
   # ----- API ------
   path('api/', include('api.urls')),
   path('doctor/', include('doctor.urls')),
   path('patient/', include('patient.urls')),
   path('admin/', admin.site.urls),
   path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
   # ------ AUTH -----
   path('signup/', user_register_view, name='signup'),
   path('login/', user_login, name='login'),
   path('logout/', user_logout, name='logout'),
   path('select-role/', role_selector, name='select-role'),
   path('patient-dashboard/', patient_dashboard, name='patient-dashboard'),
   path('medical-professional-dashboard/', med_pro_dashboard, name='medical-professional-dashboard'),
   path('silk/', include('silk.urls', namespace='silk')), # for api optimization during development
   # ----- swagger-UI ----
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
] 
if settings.DEBUG:
   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)