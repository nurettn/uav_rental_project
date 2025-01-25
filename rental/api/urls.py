from django.urls import include, path
from rest_framework import routers

from .views import (AircraftViewSet, AssemblyViewSet, PartViewSet,
                    PersonnelViewSet, TeamViewSet)

router = routers.DefaultRouter()
router.register(r"teams", TeamViewSet)
router.register(r"personnel", PersonnelViewSet)
router.register(r"aircraft", AircraftViewSet)
router.register(r"parts", PartViewSet)
router.register(r"assemblies", AssemblyViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
