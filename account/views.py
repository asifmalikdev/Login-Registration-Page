from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.status import HTTP_201_CREATED
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .throttles import RegistrationThrottleRate, LoginThrottleRate
from account.serializers import UserRegistrationSerializer, UserLoginSerializer


class UserRegistrationView(APIView):
    throttle_classes = [RegistrationThrottleRate]
    def get(self, request, format=None):
        return Response({"msg": "Send a POST request to register"})

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"msg":"Registration Successfull"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    throttle_classes = [LoginThrottleRate]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        # print(serialiier)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            print(email, password)
            user=authenticate(email=email, password = password)
            print("this is user", user)
            if user is not None:
                return Response({"msg":"Login Successfull"}, status = status.HTTP_200_OK)
            else:
                return Response({"errors": {'non_fields_errors':['Email or Passowrd is not valid']}}, status = status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)