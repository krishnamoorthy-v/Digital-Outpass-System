import json
from .controller import insertOne, getOneByEmail, getOneById, updateOneById, deleteOneById, getAll, filter_Dpt_Wise
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny


# Create your views here.

@api_view(["POST"])
@permission_classes((AllowAny,))
def setStudent(request):
    '''
    To insert the data into data base
    :param request:
    :return: status of the insert data
    '''
    print(request.data)
    if request.data["guardian_mobile"] == "":
        request.data["guardian_mobile"] = None
    res = insertOne(request.data)
    return res


@api_view(["GET"])
@permission_classes([AllowAny])
def getStudent(request, email):
    '''
    To get one student who's matching the given email id
    :param request:
    :param email:
    :return: json values
    '''
    res = getOneByEmail(email)
    return res

@api_view(["GET"])
@permission_classes([AllowAny])
def getStudentById(reqeust, id):

    res = getOneById(id)
    return res

@api_view(["PUT"])
@permission_classes([AllowAny])
def updateStudent(request, pk):
    '''
    To update student info based on the id
    :param request:
    :param pk:
    :return: updated info
    '''
    print("hi")
    data = json.loads(request.body)
    res = updateOneById(pk, data)
    return res


@api_view(["DELETE"])
@permission_classes([AllowAny])
def deleteStudent(request, pk):
    '''
    To delete the student infor based on the id
    :param request:
    :param pk:
    :return: status info
    '''
    res = deleteOneById(pk)
    return res


@api_view(["GET"])
@permission_classes([AllowAny])
def getAllStudent(request):
    '''
    to get list of all student from the db
    :param request:
    :return: list of json
    '''
    res = getAll()
    return res


@api_view(["GET"])
@permission_classes([AllowAny])
def getAllFromDpt(request, dpt):
    '''
    To get all student based on dept
    :param request:
    :param dpt:
    :return: list of the json
    '''
    res = filter_Dpt_Wise(dpt)
    return res
