from django.shortcuts import render
from rest_framework.status import HTTP_201_CREATED
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .throttles import RegistrationThrottleRate
from account.serializers import UserRegistrationSerializer


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
