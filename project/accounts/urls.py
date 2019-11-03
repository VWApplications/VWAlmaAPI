from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('', views.UserViewSet, basename="user")

urlpatterns = router.urls
