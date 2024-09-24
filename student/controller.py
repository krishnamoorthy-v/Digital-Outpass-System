from django.db import IntegrityError
from django.http import JsonResponse
from .models import StudentModel
from .serializer import StudentSerializer, StudentUpdateSerializer
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.serializers import ValidationError



def insertOne(data):
    try:
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Data stored Successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
    except IntegrityError as e:
        return JsonResponse({"error": str(e.args[1]), "error_code": str(e.args[0])}, status=status.HTTP_409_CONFLICT)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def getOneByEmail(id):
    try:
        data = StudentModel.objects.get(email=id)
        res = StudentSerializer(data, many=False)
        return Response(res.data, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({"error": str(e), "error_code": -1}, status=status.HTTP_400_BAD_REQUEST)


def getOneById(id):
    try:
        data = StudentModel.objects.get(id=id)
        res = StudentSerializer(data, many=False)
        return Response(res.data, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({"error": str(e), "error_code": -1}, status=status.HTTP_400_BAD_REQUEST)


def updateOneById(id, data):
    try:
        serializer = StudentUpdateSerializer(data=data)
        if serializer.is_valid():
            print("hi")
            if StudentModel.objects.filter(id=id).update(**data):
                return Response({"success": "updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"failed": "Id not found"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except IntegrityError as e:
        return JsonResponse({"error": str(e.args[1]), "error_code": str(e.args[0])}, status=status.HTTP_409_CONFLICT)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def deleteOneById(pk):
    try:
        res = getOneById(pk)
        if res.status_code == 200:
            StudentModel.objects.get(id=pk).delete()
            return JsonResponse({"success": "Data deleted"}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "Data not available", "error_code": -1}, status=status.HTTP_409_CONFLICT)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def getAll():
    try:
        all = StudentModel.objects.all()
        data = StudentSerializer(all, many=True)
        return Response(data.data, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def filter_Dpt_Wise(department):
    try:
        all = StudentModel.objects.filter(department=department)
        data = StudentSerializer(all, many=True)
        return Response(data.data, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
