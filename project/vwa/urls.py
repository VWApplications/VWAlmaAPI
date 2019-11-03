from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('api-token/', jwt_views.TokenObtainPairView.as_view(), name='login'),
    path('refresh-token/', jwt_views.TokenRefreshView.as_view(), name='login'),
    path('users/', include('accounts.urls')),
    path('', include('alma.core.urls')),
    path('disciplines/', include('alma.disciplines.urls')),
    path('groups/', include('alma.groups.urls')),
    path('sections/', include('alma.sections.urls')),
    path('questions/', include('alma.questions.urls'))
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
