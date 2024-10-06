from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .controller import createController, deleteAllController, getAllController, getOneController_t_id, \
    getAllControllerByStudId, getAllControllerStatus, paginatorController, updateStatusController, generateQrController, getAllControllerRequestStatus, verifyQrController, wardenResController, getAcceptedT_id

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
def deleteAll(request):
    res = deleteAllController()
    return res


@api_view(["GET"])
@permission_classes([AllowAny])
def getAll(request):
    res = getAllController()
    return res


@api_view(["GET"])
@permission_classes([AllowAny])
def getByt_id(request, id):
    res = getOneController_t_id(id)
    return res


@api_view(["GET"])
@permission_classes([AllowAny])
def getRequestStatus(request, stud_id):
    res = getAllControllerRequestStatus(stud_id)
    return res

@api_view(["GET"])
@permission_classes([AllowAny])
def getAcceptIdStud(request, stud_id):
    res = getAcceptedT_id(stud_id)
    return res

@api_view(["GET"])
@permission_classes([AllowAny])
def getByStudId(request, id):
    res = getAllControllerByStudId(id)
    return res


@api_view(["GET"])
@permission_classes([AllowAny])
def getByStatus(request, status):
    res = getAllControllerStatus(status)
    return res


@api_view(["GET"])
@permission_classes([AllowAny])
def getBypage(request, status, entries, page):
    res = paginatorController(status, entries, page)
    return res


@api_view(["PUT"])
@permission_classes([AllowAny])
def updateStatus(request, t_id, stats):
    res = wardenResController(t_id, stats)
    return res


@api_view(["GET"])
@permission_classes([AllowAny])
def getQrCode(request, id):
    res = generateQrController(id)
    return res


@api_view(["POST"])
@permission_classes([AllowAny])
def verifyQr(request):
    res = verifyQrController(request.data)
    return res
