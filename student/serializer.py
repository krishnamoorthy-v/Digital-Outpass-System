from rest_framework import serializers
from .models import StudentModel
import re
def validate_mobileNum(data):
    print("from validation", data)
    pattern = r'^[6-9]\d{9}$'
    match = re.match(pattern, str(data))
    if not match:
        raise serializers.ValidationError("Invalid mobile number")
    return data


class StudentSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(max_length=10, validators=[validate_mobileNum])
    parent_mobile = serializers.CharField(max_length=10, validators=[validate_mobileNum])
    guardian_mobile = serializers.CharField(max_length=10, validators=[validate_mobileNum])
    class Meta:
        model = StudentModel
        fields = "__all__"
