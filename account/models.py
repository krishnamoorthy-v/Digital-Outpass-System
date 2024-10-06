from django.db import models


# Create your models here.

class PasswordResetModel(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=30, null=False, blank=False, unique=True)
    token = models.TextField(max_length=20, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "password_reset"


class LoginModel(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=30, null=False, blank=False, unique=True)
    username = models.CharField(max_length=20, null=False, blank=False)
    password = models.CharField(max_length=512)
    is_active = models.BooleanField(default=False)
    user_type = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)



    class Meta:
        db_table = "login_table"
