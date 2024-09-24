from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .controller import createController, deleteAllController

# Create your views here.

@api_view(["POST"])
@permission_classes([AllowAny])
def create(request):
    data = request.data
    print(data)
    res = createController(data)
    return res

@api_view(["DELETE"])
@permission_classes([AllowAny])
def delete(request):
    res = deleteAllController()
    return res