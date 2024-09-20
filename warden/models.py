from django.db import models


# Create your models here.
class WardenModel(models.Model):
    name = models.CharField(max_length=20, null=False, unique=True)
    number = models.BigIntegerField(null=False, blank=False, unique=True)

    class Meta:
        db_table = "warden"
