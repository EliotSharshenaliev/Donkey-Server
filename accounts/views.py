from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import UserModel
from .serializers import SignUpSerializer, RegisterBoxSerializer, CurrentUserSerializer


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {"message": "User Created Successfully", "data": serializer.data}
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []
    serializer_class = CurrentUserSerializer

    def post(self, request: Request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request=request, user=user)
            serializer = self.serializer_class(user)
            return Response(serializer.data)
        return Response(
            data={
                "type": "error",
                "message": "Invalid email or password",
                "isAuth": False,
            },
            status=status.HTTP_404_NOT_FOUND)


class GetUser(APIView):
    serializer_class = CurrentUserSerializer

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            serializer = self.serializer_class(user)
            return Response(serializer.data)
        return Response(
            data={
                "message": "You've have not authenticated"
            },
            status=status.HTTP_200_OK)


class LogOutView(APIView):
    permission_classes = []

    def get(self, request: Request):
        if request.user.is_authenticated:
            logout(request=request)
            return Response(
                data={
                    "message": "Logout Successfully"
                },
                status=status.HTTP_200_OK
            )
        return Response(
            data={
                "message": "You've have not authenticated"
            },
            status=status.HTTP_200_OK
        )


class RegisterBoxListCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = RegisterBoxSerializer
