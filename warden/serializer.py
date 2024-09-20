from rest_framework import serializers
from .models import WardenModel
import re


def validate_mobileNum(data):
    print("from validation", data)
    pattern = r'^[6-9]\d{9}$'
    match = re.match(pattern, str(data))
    if not match:
        raise serializers.ValidationError("Invalid mobile number")
    return data


class WardenSerializer(serializers.ModelSerializer):
    number = serializers.CharField(max_length=10, validators=[validate_mobileNum])

    class Meta:
        model = WardenModel
        fields = '__all__'
