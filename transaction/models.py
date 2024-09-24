from django.db import models
from django.apps import apps
from student.models import StudentModel

# StudentModel = apps.get_model('student', 'StudentModel')
# Create your models here.
STATUS_CHOICES = [
    ('P', 'Pending'),
    ('C', 'Completed'),
    ('S', 'Success'),
    ('F', 'Failed'),
]


class TransactionModel(models.Model):
    t_id = models.BigAutoField(primary_key=True)
    out_time = models.DateTimeField(null=False, blank=False)
    in_time = models.DateTimeField(null=False, blank=False)
    reason = models.CharField(max_length=50, null=False, blank=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    hostel_id = models.ForeignKey(StudentModel, on_delete=models.CASCADE)

    class Meta:
        db_table = "transaction"
