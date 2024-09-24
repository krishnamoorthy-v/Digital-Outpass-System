from rest_framework.response import Response
from rest_framework import status
from .serializer import TransactionSerializer
from .models import TransactionModel
from .validation import Validation
import datetime
import re
from student.models import StudentModel
from django.core.paginator import Paginator

validate = Validation()


def createController(data):
    try:
        student = StudentModel.objects.get(id=data["hostel_id"])
        today_stud_req = TransactionModel.objects.filter(hostel_id=student)
        serializer = TransactionSerializer(today_stud_req, many=True)

        count = 0
        for i in serializer.data:

            if datetime.datetime.strptime(i["out_time"],
                                          "%Y-%m-%dT%H:%M:%SZ").date() == datetime.datetime.today().date():
                count += 1
                print(count)
            if count > 2:
                raise Exception("today out pass limit exceeds")

        validate.validate_date(data["in_time"])
        info = re.match(validate.date_regex, data["in_time"])
        #  print(info)
        year, month, day, hour, minute = info.groups()
        data["in_time"] = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour),
                                            minute=int(minute), tzinfo=datetime.UTC)

        validate.validate_date(data["out_time"])
        info = re.match(validate.date_regex, data["out_time"])
        # print(info)
        year, month, day, hour, minute = info.groups()
        data["out_time"] = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour),
                                             minute=int(minute), tzinfo=datetime.UTC)

        # print(data["out_time"].date(), ">>>", datetime.datetime.today().date())
        if data["in_time"].date() < datetime.datetime.today().date():
            raise Exception("invalid in time date")
        if data["in_time"].time() < data["out_time"].time() and data["in_time"].date() == data["out_time"].date():
            raise Exception("invalid in_time timing")
        if data["out_time"].date() < datetime.datetime.today().date():
            raise Exception("invalid out time")
        if data["out_time"].date() == datetime.datetime.today().date():
            if data["out_time"].time() > datetime.datetime.now().time():
                raise Exception("in_time must be greater than out_time")

        if data["out_time"].date() > datetime.datetime.now().date():
            raise Exception("invalid in in time")

        TransactionModel(in_time=data["in_time"], out_time=data["out_time"], reason=data["reason"],
                         hostel_id=student).save()

        return Response({"success": "data stored"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": e.args}, status=status.HTTP_409_CONFLICT)


def deleteAllController():
    try:
        TransactionModel.objects.filter().delete()
        return Response({"success": "data deleted"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)


def getAllController():
    try:
        data = TransactionModel.objects.filter()
        res = TransactionSerializer(data, many=True)
        return Response(res.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)


def getOneController_t_id(id):
    try:
        # print(id)
        data = TransactionModel.objects.filter(t_id=id)
        # print(dir(data))
        res = TransactionSerializer(data, many=True)
        # print(res)
        return Response(res.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": e.args}, status=status.HTTP_409_CONFLICT)


def getAllControllerByStudId(id):
    try:
        data = TransactionModel.objects.filter(hostel_id=id)
        res = TransactionSerializer(data, many=True)
        return Response(res.data, status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": e.args}, status=status.HTTP_409_CONFLICT)


def getAllControllerStatus(stat):
    try:
        data = TransactionModel.objects.filter(status=stat)
        res = TransactionSerializer(data, many=True)
        return Response(res.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": e.args}, status=status.HTTP_409_CONFLICT)


def paginatorController(stats, entities, page):
    try:
        if stats in ["all", "pending", "failed", "completed", "success"]:
            if stats == "all":
                data = TransactionModel.objects.filter()
            else:
                data = TransactionModel.objects.filter(status=stats)
        else:
            raise Exception("Invalid status option ")
        pages = Paginator(data, entities)
        res = TransactionSerializer(pages.page(page), many=True)
        return Response(res.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": e.args}, status=status.HTTP_409_CONFLICT)


def updateStatusController(t_id, stats):
    try:
        if TransactionModel.objects.filter(t_id=t_id).update(status=stats):
            return Response({"success": "status updated"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "transaction not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": e.args}, status=status.HTTP_409_CONFLICT)


