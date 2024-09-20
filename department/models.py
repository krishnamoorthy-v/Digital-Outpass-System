from django.db import models



# Create your models here.

class DepartmentModel(models.Model):
    dept_id = models.CharField(max_length=10, primary_key=True, null=False, unique=True)
    dept_name = models.CharField(max_length=30, null=False, unique=True)
    staff_name = models.CharField(max_length=30, null=False)
    staff_mobile = models.BigIntegerField(null=False, unique=True)

    class Meta:
        db_table = "department"
