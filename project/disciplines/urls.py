from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('disciplines', views.DisciplineViewSet, basename="discipline")

urlpatterns = router.urls