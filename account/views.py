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

# Create your views here.


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    try:
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        user_type = "student"
        LoginModel.objects.create(username=username, email=email, password=password, user_type=user_type,
                                  is_active=True).save()
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

        user = LoginModel.objects.get(email=res.data[0]["email"])
        if user.password != password:
            raise serializers.ValidationError("invalid username or password")
        if user is not None:
            refresh = RefreshToken.for_user(user)
            login_serializer = LoginSerializer(user, many=False)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': login_serializer.data
            })
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({"error": e.args[0]}, status=status.HTTP_409_CONFLICT)

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
        if (len(records) == 0):
            print("token created")
            PasswordResetModel.objects.create(email=email, token=token).save()
        else:
            print("token updated")
            PasswordResetModel.objects.filter(email=email).update(token=token)
        url = f"http://127.0.0.1:8000/account/auth/reset/{token}"
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
        token_obj = PasswordResetModel.objects.filter(token=token).first()
        # print( datetime.datetime.now().tzname(), " - token_obj.created_at")
        # print("datetime.datetime.now() -", token_obj.created_at.tzname())
        if token_obj and (
                datetime.datetime.now().utcnow() - token_obj.created_at.utcnow()).total_seconds() < 60 * 60 * 60:
            print("hi: ",token_obj.email)
            LoginModel.objects.filter(email=token_obj.email).update(password=password)
            token_obj.delete()
            return Response({"success:", "password update"}, status=status.HTTP_200_OK)
        else:
            return Response({"error:", "token expired"}, status=status.HTTP_408_REQUEST_TIMEOUT)
    except Exception as e:
        return Response({"error:", e.args[0]}, status=status.HTTP_400_BAD_REQUEST)


