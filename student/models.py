from django.db import models

# Create your models here.

class StudentModel(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    email = models.EmailField(max_length=50, blank=False, unique=True, null=False)
    mobile = models.BigIntegerField(unique=True, null=True)
    profile = models.TextField()
    department = models.CharField(max_length=20, blank=False, null=False)

    parent_name = models.CharField(max_length=30, blank=False, null=False)
    parent_mobile = models.BigIntegerField(unique=True, null=True)

    guardian_name = models.CharField(max_length=30, blank=False, null=False)
    guardian_mobile = models.BigIntegerField(unique=True, null=True)

    home_addr = models.CharField(max_length=256, blank=False, null=False)

    class Meta:
        db_table = "student"



