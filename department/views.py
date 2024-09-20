from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .controller import getInfoById, insertOne, updateOne, deleteOne, getAll
from rest_framework.permissions import AllowAny

# Create your views here.


@api_view(["GET"])
@permission_classes([AllowAny])
def getDept(request, id):
    res = getInfoById(id)
    return res

@api_view(["POST"])
@permission_classes([AllowAny])
def setDepartment(request):
    data = request.data
    res = insertOne(data)
    return res

@api_view(["PUT"])
@permission_classes([AllowAny])
def updateInfo(request, pk):
    data = request.data
    res = updateOne(pk, data)
    return res

@api_view(["DELETE"])
@permission_classes([AllowAny])
def deleteInfo(request, pk):
    data = request.data
    res = deleteOne(pk)
    return res

@api_view(["GET"])
@permission_classes([AllowAny])
def getAllInfo(request):
    res = getAll()
    return res