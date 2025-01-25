from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    # Parts CRUD URLs
    path("parts/", views.part_list, name="part_list"),
    path("parts/create/", views.part_create, name="part_create"),
    path("parts/<int:pk>/edit/", views.part_update, name="part_update"),
    path("parts/<int:pk>/delete/", views.part_delete, name="part_delete"),
    # Assembly URLs
    path("assemblies/", views.assembly_list, name="assembly_list"),
    path("assemblies/assemble/", views.assemble_aircraft, name="assemble_aircraft"),
]
