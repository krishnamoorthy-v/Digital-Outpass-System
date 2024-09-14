import json

from django.http import HttpResponse, JsonResponse
from django.middleware import csrf

from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from .controller import insertOne, getOneByEmail, updateOneById, deleteOneById, getAll, filter_Dpt_Wise


# Create your views here.


def setStudent(request):
    if request.method == "POST":
        res = insertOne(json.loads(request.body))
        return res
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def getStudent(request, email):
    if request.method == "GET":
        res = getOneByEmail(email)
        return res
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)



def updateStudent(request, pk):
    if request.method == "PUT":
        data = json.loads(request.body)
        res = updateOneById(pk, data)
        return res
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def deleteStudent(request, pk):

    if request.method == "DELETE":
        res = deleteOneById(pk)
        return res
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def getAllStudent(request):

    if request.method == "GET":
        res = getAll()
        return res
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def getAllFromDpt(request, dpt):

    if request.method == "GET":
        res = filter_Dpt_Wise(dpt)
        return res
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
