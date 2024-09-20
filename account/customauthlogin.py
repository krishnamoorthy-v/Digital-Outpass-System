from django.contrib.auth.backends import BaseBackend
from .models import LoginModel
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class CustomAuthLogin(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # You can authenticate by username or email, depending on your logic
            user = LoginModel.objects.get(username=username)

            # Check password manually, since Django will not handle it for custom models
            if user.password == password and user.is_active:
                return user
        except LoginModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return LoginModel.objects.get(pk=user_id)
        except LoginModel.DoesNotExist:
            return None
