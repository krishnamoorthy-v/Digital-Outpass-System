from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import authenticate
from .serializer import LoginSerializer
from django.core.mail import send_mail
from .models import PasswordResetModel, LoginModel
import datetime
from .controller import generateToken
from django.http import HttpResponse
from argon2 import PasswordHasher
import argon2

ph = PasswordHasher()


# Create your views here.
@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request, usertype="student"):
    try:
        if usertype.lower() in ["student", "warden", "security", "admin"]:
            username = request.data.get("username")
            email = request.data.get("email")
            password = ph.hash(request.data.get("password"))
            user_type = usertype

            LoginModel.objects.create(username=username, email=email, password=password, user_type=user_type,
                                      is_active=True).save()
        else:
            return Response({"failed": "invalid user type"})
        return Response({"Success": "account created Successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error:", e.args}, status=status.HTTP_409_CONFLICT)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    try:
        email = request.data.get("email")
        password = request.data.get("password")

        data = LoginModel.objects.filter(email=email)
        res = LoginSerializer(data, many=True)
        # print(res.data[0]["email"])
        if res.data:

            user = LoginModel.objects.get(email=res.data[0]["email"])

            # print(user.password)

            if user is not None and ph.verify(user.password, password):
                request.session["login_id"] = user.id
                request.session["email"] = user.email
                request.session["user_type"] = user.user_type
                request.session.set_expiry(60 * 60)

                login_serializer = LoginSerializer(user, many=False)
                print(login_serializer.data)
                user = {
                    "user": login_serializer.data
                }
                return Response(user, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            raise Exception("Invalid email id")
    except argon2.exceptions.VerifyMismatchError:
        return Response({"error": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": e.args}, status=status.HTTP_409_CONFLICT)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def resetPassword(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")
        new_password = request.data.get("new_password")
        confirm_new_password = request.data.get("confirm_new_password")

        if new_password != confirm_new_password:
            raise serializers.ValidationError("new password and confirm password are not same")
        user = authenticate(username=username, password=password)
        if user is not None:
            user.set_password(new_password)
            user.save()

        else:
            raise serializers.ValidationError("Invalid username or password ")
        return Response({"success": "password reset successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": e.detail[0]}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def password_reset_email(request, email):
    try:

        data = LoginModel.objects.filter(email=email).first()

        res = LoginSerializer(data, many=False)
        # res.data["last_login"] = res.data["created_at"]

        token = generateToken()
        # print("HI")
        records = PasswordResetModel.objects.filter(email=email)
        if len(records) == 0:
            print("token created")
            PasswordResetModel.objects.create(email=email, token=token).save()
        else:
            print("token updated")
            PasswordResetModel.objects.filter(email=email).update(token=token)
        url = f"http://192.168.63.110:3000/account/auth/reset/{token}"
        send_mail(
            'DOS password reset',
            'click the below link for reset password ' + url,
            'digitaloutpasssystem@gmail.com',
            [email],
            fail_silently=True,
            # fail_silently: A boolean value that indicates whether to raise an exception if the email fails to send.
        )
        return Response({"success": "check your email"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": e.args}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([AllowAny])
def password_reset_confirm(request, token):
    try:
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")
        if password != confirm_password:
            raise Exception("Password and Confirm password not matching")

        token_obj = PasswordResetModel.objects.filter(token=token).first()
        # print( datetime.datetime.now().tzname(), " - token_obj.created_at")
        # print("datetime.datetime.now() -", token_obj.created_at.tzname())
        if token_obj and (
                datetime.datetime.now().utcnow() - token_obj.created_at.utcnow()).total_seconds() < 60 * 60 * 60:
            print("hi: ", token_obj.email)
            LoginModel.objects.filter(email=token_obj.email).update(password=ph.hash(password))
            token_obj.delete()
            return Response({"success": "password update"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "token expired"}, status=status.HTTP_408_REQUEST_TIMEOUT)
    except Exception as e:
        return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([AllowAny])
def deleteByid(request, id):
    try:
        res = LoginModel.objects.filter(id=id).delete()

        if res[0]:
            return Response({"success": "data deleted"}, status=status.HTTP_200_OK)
        else:
            raise Exception("no data found")
    except Exception as e:
        return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)
