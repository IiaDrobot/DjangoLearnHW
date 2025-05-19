from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
import datetime

def set_jwt_cookies(response, user):
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    access_expiry = datetime.datetime.fromtimestamp(access_token['exp'], datetime.timezone.utc)
    refresh_expiry = datetime.datetime.fromtimestamp(refresh['exp'], datetime.timezone.utc)

    response.set_cookie(
        key='access_token',
        value=str(access_token),
        httponly=True,
        secure=False,  # True в продакшене с https
        samesite='Lax',
        expires=access_expiry
    )
    response.set_cookie(
        key='refresh_token',
        value=str(refresh),
        httponly=True,
        secure=False,
        samesite='Lax',
        expires=refresh_expiry
    )


class LogInAPIView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            response = Response({"message": "Успешный вход"}, status=status.HTTP_200_OK)
            set_jwt_cookies(response, user)
            return response
        return Response({"error": "Неверный логин или пароль"}, status=status.HTTP_401_UNAUTHORIZED)
