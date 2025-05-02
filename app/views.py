from django.contrib.auth import authenticate
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return Response({"data": user.username, "msg": "Siz ro'yxatdan o'tdingiz!"})


class LoginView(APIView):
    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']

        user = authenticate(username= username, password= password)
        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = JWTAuthentication,

    def post(self, request):
        try:
            r_token = request.data['refresh']
            token = RefreshToken(r_token)
            token.blacklist()
            return Response({
                "message": "Tizimdan chiqdingiz!"
            })
        except Exception:
            return Response({
                "message": "Token noto'g'ri!"
            })