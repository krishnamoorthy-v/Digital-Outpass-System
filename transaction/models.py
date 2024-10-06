from django.db import models
from django.apps import apps
from student.models import StudentModel

# StudentModel = apps.get_model('student', 'StudentModel')
# Create your models here.
STATUS_CHOICES = [
    ('P', 'Pending'),
    ('A', 'Accepted'),
    ('R', 'Rejected'),
    ('CI', 'Check_In'),
    ('CO', 'Check_Out'),
    ('C', 'Completed'),
    ('E', 'Expired')
]


class TransactionModel(models.Model):
    t_id = models.BigAutoField(primary_key=True)
    out_time = models.DateTimeField(null=False, blank=False)
    in_time = models.DateTimeField(null=False, blank=False)
    reason = models.CharField(max_length=50, null=False, blank=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    hostel_id = models.ForeignKey(StudentModel, on_delete=models.CASCADE)
    actual_in_time = models.DateTimeField(null=True)
    actual_out_time = models.DateTimeField(null=True)
    token = models.CharField(max_length=130, null=True)
    token_expire = models.DateTimeField(null=True)
    qr_code_base_64 = models.TextField(null=True)

    class Meta:
        db_table = "transaction"
