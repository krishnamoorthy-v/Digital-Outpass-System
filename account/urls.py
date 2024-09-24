from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
urlpatterns = [

    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/signup', views.signup),
    path('auth/login', views.login),
    path('auth/reset/<str:email>', views.password_reset_email),
    path('auth/reset/confirm/<str:token>', views.password_reset_confirm),


]
