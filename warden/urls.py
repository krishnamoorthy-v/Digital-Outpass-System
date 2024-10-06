from django.urls import path
from . import views
urlpatterns = [
    path('create', views.create),
    path('readall', views.readAll),
    path('read/email/<str:email>', views.readOneByEmail),
    path('read/email', views.readOneByEmailSession),
    path('read/id/<int:id>', views.readOneById),
    path('update/id/<int:id>', views.updateOneById),
    path('update/email/<str:email>', views.updateOneByEmail),
    path('delete/email/<str:email>', views.deleteOneByEmail),
    path('delete/id/<int:id>', views.deleteOneById),
    path('delete/all', views.deleteAll)
]