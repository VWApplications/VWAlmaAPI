from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('api-token/', jwt_views.TokenObtainPairView.as_view(), name='login'),
    path('refresh-token/', jwt_views.TokenRefreshView.as_view(), name='login'),
    path('', include('core.urls')),
    path('users/', include('accounts.urls')),
    path('disciplines/', include('disciplines.urls'))
]

# While in development mode we will use relative URL for static and average
# files. In production mode we will no longer need this folder as we will store
# everything on a server
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
