from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('', views.DisciplineViewSet, basename="discipline")

urlpatterns = router.urls