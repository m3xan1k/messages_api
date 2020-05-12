from users.serializers import RegistrationSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class UsersView(APIView):

    name = 'users'

    def post(self, request: Request) -> Response:
        """
        Creates new user
        """
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: Request) -> Response:
        """
        Returns all users
        """
        queryset = User.objects.all()
        serializer = UserSerializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserView(APIView):

    name = 'user'

    def get(self, request: Request, id: str) -> Response:
        if not id.isnumeric():
            return Response(data={'err': 'id should be numeric'},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        user = get_object_or_404(User, id=int(id))
        serializer = UserSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginView(APIView):

    name = 'login'

    def post(self, request: Request) -> Response:
        pass
