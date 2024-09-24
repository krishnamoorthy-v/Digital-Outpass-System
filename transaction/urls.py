from django.urls import path
from . import views

urlpatterns = [
    path("create", views.create),
    path("deleteall", views.delete),
    path("getall", views.getAll),
    path("getbyid/<int:id>", views.getByt_id),
    path("getbystud/<int:id>", views.getByStudId),
    path("getstatus/<str:status>", views.getByStatus),
    path("paginator/<str:status>/<int:entries>/<int:page>", views.getBypage),
    path("update/<int:t_id>/<str:stats>", views.updateStatus),
]