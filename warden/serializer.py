from rest_framework import serializers
from .models import WardenModel
import re
import base64


def validate_mobileNum(data):
    print("from validation", data)
    pattern = r'^[6-9]\d{9}$'
    match = re.match(pattern, str(data))
    if not match:
        raise serializers.ValidationError("Invalid mobile number")
    return data


def validate_base64(value):
    try:
        base64.b64decode(value, validate=True)
        return value
    except Exception:
        raise serializers.ValidationError("Image expected")


def validate_email_update(value):
    # print(dir(id))

    # data = WardenModel.objects.get(id=id)
    # if data.email == value:
    #     return value
    if value != '':
        data = WardenModel.objects.filter(email=value)
        if len(data) == 0:
            return value
        else:
            raise serializers.ValidationError("email id already exits")


def validate_email(value):
    if WardenModel.objects.filter(email=value).exists():
        raise serializers.ValidationError('This email already exists.')
    return value


class WardenSerializer(serializers.ModelSerializer):
    primary_number = serializers.CharField(max_length=10, validators=[validate_mobileNum])
    email = serializers.EmailField(validators=[validate_email])
    profile = serializers.CharField(required=False, validators=[validate_base64])

    class Meta:
        model = WardenModel
        fields = '__all__'


# class WardenUpdateSerializer(serializers.ModelSerializer):
#     primary_number = serializers.CharField(required=False, max_length=10, validators=[validate_mobileNum])
#     email = serializers.EmailField(required=False, validators=[validate_email_update])
#     profile = serializers.CharField(required=False, validators=[validate_base64])
#
#     class Meta:
#         model = WardenModel
#         fields = '__all__'
