from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register('news', views.NewsViewSet, basename="new")
router.register('tags', views.TagsViewSet, basename="tag")

urlpatterns = [
    path("contact/", views.ContactViewSet.as_view(), name="contact"),
    path('', include(router.urls))
]