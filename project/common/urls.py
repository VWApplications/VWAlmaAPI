from django.urls import path
from . import views

urlpatterns = [
    path("generate/", views.GeneratePDFView.as_view(), name="generate")
]