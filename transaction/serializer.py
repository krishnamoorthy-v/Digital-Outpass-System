from rest_framework import serializers
from .models import TransactionModel
# STATUS_CHOICES = [
#     ('P', 'Pending'),
#     ('C', 'Completed'),
#     ('CI', 'Check_In'),
#     ('CO', 'Check_Out'),
#     ('S', 'Success'),
#     ('F', 'Failed'),
# ]

class TransactionSerializer(serializers.ModelSerializer):
    # status = serializers.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    class Meta:
        model = TransactionModel
        fields = "__all__"
