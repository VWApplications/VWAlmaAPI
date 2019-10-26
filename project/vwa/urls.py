from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('api-token/', jwt_views.TokenObtainPairView.as_view(), name='login'),
    path('refresh-token/', jwt_views.TokenRefreshView.as_view(), name='login'),
    path('', include('core.urls')),
    path('users/', include('accounts.urls')),
    path('disciplines/', include('disciplines.urls')),
    path('groups/', include('groups.urls')),
    path('sections/', include('sections.urls')),
    path('questions/', include('questions.urls'))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
