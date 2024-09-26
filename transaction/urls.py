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
    path("warden/update/<int:t_id>/<str:stats>", views.updateStatus),
    path("qrcode/generating/<int:id>", views.getQrCode),
    path("qrcode/verify", views.verifyQr),
    path("getstatus/student/<int:stud_id>", views.getRequestStatus)


]