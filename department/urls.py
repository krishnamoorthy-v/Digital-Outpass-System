from django.urls import path
from . import views


urlpatterns = [
    path("get/<str:id>", views.getDept),
    path("create", views.setDepartment),
    path("update/<str:pk>", views.updateInfo),
    path("delete/<str:pk>", views.deleteInfo),
    path("getall", views.getAllInfo)
]