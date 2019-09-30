from django.urls import path, include, re_path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('', views.UserViewSet, basename="user")

urlpatterns = [
    re_path(
      r"^change_photo/(?P<filename>[-a-zA-Z0-9_]+.[a-z]{3})/$",
      views.UserUploadPhotoView.as_view(),
      name="change-photo"
    ),
    path('', include(router.urls))
]