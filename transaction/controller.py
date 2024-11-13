from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from .serializer import TransactionSerializer
from .models import TransactionModel
from .validation import Validation
import datetime
import re
from student.models import StudentModel
from django.core.paginator import Paginator
from .services import generateQrCode
import json

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
            if count > 0:
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
            print(data["out_time"].time(), ">", datetime.datetime.now().time())
            if data["out_time"].time() < datetime.datetime.now().time():
                raise Exception("invalid out_time")

        # to check out date must be lesser than current date than raise the error
        if data["out_time"].date() < datetime.datetime.now().date():
            raise Exception("invalid in out date")

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
        serializer = TransactionSerializer(data, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": e.args}, status=status.HTTP_409_CONFLICT)


def getAllControllerRequestStatus(id):
    try:
        data = TransactionModel.objects.filter(hostel_id=id).filter(Q(status="pending") | Q(status="accepted"))
        if data:
            serializer = TransactionSerializer(data, many=True)
            res = {"t_id": serializer.data[-1]["t_id"], "out_time": serializer.data[-1]["out_time"],
                   "in_time": serializer.data[-1]["in_time"], "reason": serializer.data[-1]["reason"],
                   "status": serializer.data[-1]["status"], "hostel_id": serializer.data[-1]["hostel_id"]}
            return Response(res, status.HTTP_200_OK)
        else:
            return Response({"error": "no transaction found"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": e.args}, status=status.HTTP_409_CONFLICT)


def getAllControllerStatus(stats):
    try:
        if stats in ["all", "pending", "rejected", "completed", "accepted"]:
            if stats == "all":
                data = TransactionModel.objects.filter()
            else:
                data = TransactionModel.objects.filter(status=stats)
            res = TransactionSerializer(data, many=True)
            return Response(res.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "invalid status code"}, status=status.HTTP_409_CONFLICT)
    except Exception as e:
        return Response({"error": e.args}, status=status.HTTP_409_CONFLICT)


def getAcceptedT_id(stud_id):
    try:
        data = TransactionModel.objects.filter(hostel_id=stud_id).filter(status="accepted")
        res = TransactionSerializer(data, many=True)
        if res.data:
            return Response(res.data, status=status.HTTP_200_OK)
        else:
            raise Exception("Warden not accepted you invitation")
    except Exception as e:
        return Response({"error": e.args}, status=status.HTTP_409_CONFLICT)


def paginatorController(stats, entities, page):
    try:
        if stats in ["all", "pending", "rejected", "completed", "accepted"]:
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
        if stats.lower() not in ["expired", "pending", "rejected", "completed", "accepted", "check_out", "check_in"]:
            raise Exception("Invalid status option")
        if TransactionModel.objects.filter(t_id=t_id).update(status=stats):
            return Response({"success": "status updated"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "transaction not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": e.args}, status=status.HTTP_409_CONFLICT)


def wardenResController(t_id, stats):
    try:
        if stats.lower() not in ["rejected", "accepted"]:
            raise Exception("Invalid status option")
        if TransactionModel.objects.filter(t_id=t_id).filter(status="pending"):
            if TransactionModel.objects.filter(t_id=t_id).update(status=stats):
                return Response({"success": "status updated"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "transaction not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "invalid operation approval"}, status=status.HTTP_409_CONFLICT)
    except Exception as e:
        return Response({"error": e.args}, status=status.HTTP_409_CONFLICT)


def generateQrController(t_id):
    try:
        data = TransactionModel.objects.filter(t_id=t_id).filter(status="accepted")
        if data:
            serializer = TransactionSerializer(data[0], many=False)

            if datetime.datetime.strptime(serializer.data["out_time"],
                                          "%Y-%m-%dT%H:%M:%SZ").date() < datetime.datetime.today().date():
                TransactionModel.objects.filter(t_id=t_id).filter(status="accepted").update(status="Expired")
                raise Exception("Request Expires")
            else:
                info, qr_base64 = generateQrCode(serializer.data, 60)
                print(info)
                if TransactionModel.objects.filter(t_id=t_id).filter(status="accepted").update(token=info["token"],
                                                                                               qr_code_base_64=qr_base64,
                                                                                               token_expire=info[
                                                                                                   "expire"]):
                    print("Log: Transaction Controller qr code updated on table")
                else:
                    print("Log: Transaction Controller qr not updated on table")
            return Response({"QRcode": qr_base64}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Warden not allowed you to go out"}, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)


def verifyQrController(info):
    try:

        data = TransactionModel.objects.filter(token=info["token"]).filter(status="accepted")
        res = TransactionSerializer(data, many=True)
        all_data = res.data

        if all_data:
            # print(data)
            data = all_data[0]
            print(data)
            print(datetime.datetime.strptime(data["token_expire"],
                                             "%Y-%m-%dT%H:%M:%S.%fZ").time(), '<', datetime.datetime.today().time())
            if datetime.datetime.strptime(data["token_expire"],
                                          "%Y-%m-%dT%H:%M:%S.%fZ").time() > datetime.datetime.today().time():
                raise Exception("Qr code Expired")

            else:
                TransactionModel.objects.filter(token=data["token"]).update(
                    actual_out_time=str(datetime.datetime.now(datetime.UTC)))
                TransactionModel.objects.filter(token=data["token"]).update(status="check_out")

            return Response({"success": "Verified to Out"}, status=status.HTTP_200_OK)

        elif TransactionModel.objects.filter(token=info["token"]).filter(status="check_out"):
            TransactionModel.objects.filter(token=info["token"]).update(
                actual_in_time=str(datetime.datetime.now(datetime.UTC)))
            TransactionModel.objects.filter(token=info["token"]).update(status="check_in")
            return Response({"success": "Verified to In"}, status=status.HTTP_200_OK)

        else:
            raise Exception("Not Allowed to out")

    except Exception as e:
        return Response({"error": e.args}, status=status.HTTP_409_CONFLICT)
