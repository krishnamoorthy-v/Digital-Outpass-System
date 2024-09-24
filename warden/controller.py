from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.serializers import ValidationError
from .models import WardenModel
from .serializer import WardenSerializer
from .validation import Validation


def createController(data):
    try:
        serializer = WardenSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "data saved"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def readAllController():
    try:
        data = WardenModel.objects.all()
        res = WardenSerializer(data, many=True)
        return Response(res.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)


def readOneControllerEmail(email):
    try:
        if email != '':
            data = WardenModel.objects.get(email=email)
            res = WardenSerializer(data, many=False)
        else:
            raise ValidationError("Invalid unique Id")
        return Response(res.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error:", e.args[0]}, status=status.HTTP_400_BAD_REQUEST)


def readOneControllerId(pk):
    try:
        data = WardenModel.objects.get(id=pk)
        res = WardenSerializer(data, many=False)
        return Response(res.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error:", e.args}, status=status.HTTP_409_CONFLICT)


def updateOneControllerId(pk, data):
    try:
        validate = Validation()
        res = WardenModel.objects.get(id=pk)
        if res.primary_number != data["primary_number"]:
            res.primary_number = validate.validate_mobileNum(data["primary_number"])
            # value_exits = WardenModel.objects.filter(primary_number=data["primary_number"]).exclude(id=pk).exists()
            # print(value_exits)
        if res.email != data["email"]:
            res.email = validate.validate_email(data["email"])
            # value_exits = WardenModel.objects.filter(email=data["email"]).exclude(id=pk).exists()
            # print(value_exits)

        if res.profile != data["profile"]:
            res.profile = validate.validate_base64(data["profile"])

        if res.name != data["name"]:
            res.name = data["name"]

        if res.secondary_number != data["secondary_number"]:
            res.secondary_number = validate.validate_mobileNum(data["secondary_number"])
            # value_exits = WardenModel.objects.filter(secondary_number=data["secondary_number"]).exclude(id=pk).exists()
            # print(value_exits)
        res.save()
        print("data updating")
        return Response({"success": "data updated"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": e.args}, status=status.HTTP_409_CONFLICT)


def updateOneControllerEmail(email, data):
    try:
        validate = Validation()
        res = WardenModel.objects.get(email=email)
        if res.primary_number != data["primary_number"]:
            res.primary_number = validate.validate_mobileNum(data["primary_number"])

        if res.email != data["email"]:
            res.email = validate.validate_email(data["email"])

        if res.profile != data["profile"]:
            res.profile = validate.validate_base64(data["profile"])

        if res.name != data["name"]:
            res.name = data["name"]

        if res.secondary_number != data["secondary_number"]:
            res.secondary_number = validate.validate_mobileNum(data["secondary_number"])
        res.save()
        return Response({"success": "data updated"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": e.args}, status=status.HTTP_409_CONFLICT)


def deleteOneControllerId(id):
    try:
        WardenModel.objects.get(id=id).delete()
        return Response({"success: ": "deleted successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "data not found"}, status=status.HTTP_404_NOT_FOUND)


def deleteOneControllerEmail(email):
    try:
        WardenModel.objects.get(email=email).delete()
        return Response({"success: ": "deleted successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "data not found"}, status=status.HTTP_404_NOT_FOUND)


def deleteAllController():
    try:
        WardenModel.objects.all().delete()
        return Response({"success: ": "deleted successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "unexpected things happend during delete all operation"},
                        status=status.HTTP_404_NOT_FOUND)
