from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from .models import StudentModel
from .validator import is_indian_mobile_number
import json


def insertOne(data):
    try:
        mobile = [data["mobile"], data["parent_mobile"], data["guardian_mobile"]]

        if not is_indian_mobile_number(mobile[0]):
            raise Exception(f"Invalid mobile number {mobile[0]}")
        if not is_indian_mobile_number(mobile[1]):
            raise Exception(f"Invalid mobile number {mobile[1]}")
        if not is_indian_mobile_number(mobile[2]):
            raise Exception(f"Invalid mobile numbe {mobile[2]}r")

        StudentModel(name=data["name"], email=data["email"], mobile=data["mobile"], profile=data["profile"],
                     department=data["department"], parent_name=data["parent_name"],
                     parent_mobile=data["parent_mobile"],
                     guardian_name=data["guardian_name"], guardian_mobile=data["guardian_mobile"],
                     home_addr=data["home_addr"]
                     ).save()
        return JsonResponse({"success": "Data Retrived Successfully"}, status=200)
    except IntegrityError as e:
        return JsonResponse({"error": str(e.args[1]),
                             "error_code": str(e.args[0])
                             }, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def getOneByEmail(id):
    try:
        data = StudentModel.objects.get(email=id)
        res = {
            "id": data.pk,
            "name": data.name,
            "email": data.email,
            "mobile": data.mobile,
            "profile": data.profile,
            "department": data.department,
            "parent_name": data.parent_name,
            "parent_mobile": data.parent_mobile,
            "guardian_name": data.guardian_name,
            "guardian_mobile": data.guardian_mobile,
            "home_addr": data.home_addr
        }

        return JsonResponse(res, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e), "error_code": -1}, status=500)


def getOneById(id):
    try:
        data = StudentModel.objects.get(id=id)
        res = {
            "id": data.pk,
            "name": data.name,
            "email": data.email,
            "mobile": data.mobile,
            "profile": data.profile,
            "department": data.department,
            "parent_name": data.parent_name,
            "parent_mobile": data.parent_mobile,
            "guardian_name": data.guardian_name,
            "guardian_mobile": data.guardian_mobile,
            "home_addr": data.home_addr
        }

        return JsonResponse(res, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e), "error_code": -1}, status=500)


def updateOneById(id, data):
    try:
        res = getOneById(id)
        if res.status_code == 200:
            data = StudentModel.objects.filter(id=id).update(
                name=data["name"], email=data["email"], mobile=data["mobile"], profile=data["profile"],
                department=data["department"], parent_name=data["parent_name"],
                parent_mobile=data["parent_mobile"],
                guardian_name=data["guardian_name"], guardian_mobile=data["guardian_mobile"],
                home_addr=data["home_addr"]
            )
            return JsonResponse({"success": "Data updated"}, status=200)
        else:
            return JsonResponse({"error": "Id not found", "error_code": "-1"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def deleteOneById(pk):
    try:
        res = getOneById(pk)
        if res.status_code == 200:
            StudentModel.objects.get(id=pk).delete()
            return JsonResponse({"success": "Data deleted"}, status=200)
        else:
            return JsonResponse({"error": "Data not available", "error_code": -1}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def getAll():
    try:
        all = StudentModel.objects.all()
        data = serializers.serialize("json", all)
        return HttpResponse(data, content_type='application/json', status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def filter_Dpt_Wise(department):
    try:
        all = StudentModel.objects.filter(department=department)
        data = serializers.serialize("json", all)
        return HttpResponse(data, content_type='application/json')
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
