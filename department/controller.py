from django.http import JsonResponse

from .serializer import DepartmentSerializer
from rest_framework.response import Response
from rest_framework.views import status
from .models import DepartmentModel


def getInfoById(id):
    try:
        data = DepartmentModel.objects.get(dept_id=id)
        res = DepartmentSerializer(data, many=False)
        return Response(res.data, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def insertOne(data):
    try:
        serializer = DepartmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"success": "data stored"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def updateOne(pk, data):
    try:

        if DepartmentModel.objects.filter(dept_id=pk).update(**data):
            return Response({"success": "updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"failed": "Id not found"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)


def deleteOne(pk):
    try:
        if DepartmentModel.objects.filter(dept_id=pk).delete()[0]:
            return Response({"success": "deleted successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"failed": "Id not found"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)


def getAll():
    try:
        data = DepartmentModel.objects.all()
        res = DepartmentSerializer(data, many=True)
        return Response(res.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
