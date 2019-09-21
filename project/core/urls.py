from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('news', views.NewsViewSet, basename="new")
router.register('tags', views.TagsViewSet, basename="tag")

urlpatterns = router.urls