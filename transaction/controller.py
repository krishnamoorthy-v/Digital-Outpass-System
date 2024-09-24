from rest_framework.response import Response
from rest_framework import status
from .serializer import TransactionSerializer
from .models import TransactionModel
from .validation import Validation
import datetime
import re
from student.models import StudentModel

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
        StudentModel.objects.filter().delete()
        return Response({"success": "data deleted"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)