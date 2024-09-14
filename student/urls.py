from django.urls import path
from . import views

urlpatterns = [
    path('create', views.setStudent, name="set_student_info"),
    path('get/<str:email>', views.getStudent, name="get_student_info"),
    path('update/<int:pk>', views.updateStudent, name="update_student_info"),
    path('delete/<int:pk>', views.deleteStudent, name="delete_student"),
    path('getall', views.getAllStudent, name="get_all_student"),
    path('getall/<str:dpt>', views.getAllFromDpt, name="filter_based_dept")

]