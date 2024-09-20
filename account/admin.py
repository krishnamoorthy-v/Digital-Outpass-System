from django.contrib import admin
from .models import PasswordResetModel, LoginModel
# Register your models here.

admin.site.register(PasswordResetModel)
admin.site.register(LoginModel)