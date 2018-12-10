from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from rest_framework_swagger.views import get_swagger_view
from accounts import views as account_views
from core import views as core_views
from disciplines import views as discipline_views


router = routers.DefaultRouter()
router.register('tags', core_views.TagsViewSet, basename='tag')
router.register('news', core_views.NewsViewSet, basename='new')
router.register('users', account_views.UserViewSet, basename="user")
router.register('disciplines', discipline_views.DisciplineViewSet, basename="discipline")

# MUTABLE
schema_view = get_swagger_view(title='Restful API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view),
    path(
        'api-token/',
        jwt_views.TokenObtainPairView.as_view(),
        name='login'
    ),
    path(
        'refresh-token/',
        jwt_views.TokenRefreshView.as_view(),
        name='login'
    ),
    path(
        'api-auth/',
        include('rest_framework.urls'),
        name='rest_framework'
    ),
]

urlpatterns += router.urls

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