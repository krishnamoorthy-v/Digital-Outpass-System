from rest_framework import serializers
from .models import StudentModel
import re
import base64
import re


def validate_mobileNum(data):
    print("from validation", data)
    pattern = r'^[6-9]\d{9}$'
    match = re.match(pattern, str(data))
    if not match:
        raise serializers.ValidationError("Invalid mobile number")
    return data

def validate_mobileNum2(data):
    print("from validation 2", data)
    pattern = r'^[6-9]\d{9}$'
    match = re.match(pattern, str(data))
    if not match:
        raise serializers.ValidationError("Invalid mobile number")
    return data

def validate_base64(value):
    try:
        print("from base 64 validation")
        base64.b64decode(value, validate=True)
        return value
    except Exception:
        raise serializers.ValidationError("Image expected")


def validate_email(value):
    if StudentModel.objects.filter(email=value).exists():
        raise serializers.ValidationError('This email already exists.')
    return value


class StudentSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(max_length=10, validators=[validate_mobileNum])
    parent_mobile = serializers.CharField(max_length=10, validators=[validate_mobileNum])
    guardian_mobile = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=10, validators=[validate_mobileNum2])
    profile = serializers.CharField(required=False, validators=[validate_base64])

    class Meta:
        model = StudentModel
        fields = "__all__"


class StudentUpdateSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(max_length=10, validators=[validate_mobileNum])
    parent_mobile = serializers.CharField(max_length=10, validators=[validate_mobileNum])
    guardian_mobile = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=10, validators=[validate_mobileNum2])
    profile = serializers.CharField(required=False, validators=[validate_base64])
    # email = serializers.EmailField(required=False, validators=[lambda value: validate_email(value, StudentUpdateSerializer)])
    email = serializers.EmailField(required=False)

    class Meta:
        model = StudentModel
        fields = "__all__"
