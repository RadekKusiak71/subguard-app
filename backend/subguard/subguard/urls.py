from django.contrib import admin
from django.urls import URLPattern, include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

docs_urlpatterns: list[URLPattern] = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns: list[URLPattern] = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls'), name='users'),
] + docs_urlpatterns