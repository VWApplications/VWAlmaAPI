from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('', views.GroupViewSet, basename="group")

urlpatterns = router.urls