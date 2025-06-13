from django.shortcuts import render
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class UserRegistrationView(APIView):
    def get(self, request, format=None):
        return Response({"msg": "Send a POST request to register"})

    def post(self, request, format=None):
        print("hello asif")
        return Response({"msg": "Registration Successfull "})
