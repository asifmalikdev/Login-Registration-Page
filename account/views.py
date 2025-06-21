from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from urllib3 import request

from .throttles import RegistrationThrottleRate, LoginThrottleRate
from account.serializers import UserRegistrationSerializer, UserLoginSerializer, UserChangePasswordSerializer
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserProfileSerializer

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


class UserRegistrationView(APIView):
    throttle_classes = [RegistrationThrottleRate]
    renderer_classes = [UserRenderer]
    def get(self, request, format=None):
        return Response({"msg": "Send a POST request to register"})

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, "msg":"Registration Successfull"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    throttle_classes = [LoginThrottleRate]
    renderer_classes = [UserRenderer]


    def get(self, request, format=None):
        return Response({"msg": "Send a POST request to login"})

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            print(email, password)
            user=authenticate(email=email, password = password)
            print("this is user", user)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, "msg":"Login Successfull"}, status = status.HTTP_200_OK)
            else:
                return Response({"errors": {'non_fields_errors':['Email or Passowrd is not valid']}}, status = status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)

class UserChangePassword(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self):
        serializer = UserChangePasswordSerializer(data=request.data, context={"user":request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"password changed successfully"}, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)