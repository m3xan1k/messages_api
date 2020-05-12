from users.serializers import RegistrationSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout


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
        """
        Returns single user instance by id
        """
        if not id.isnumeric():
            return Response(data={'err': 'id should be numeric'},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        user = get_object_or_404(User, id=int(id))
        serializer = UserSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogView(APIView):

    name = 'user_log'

    def get(self, request: Request) -> Response:
        logout(request)
        return Response({'index_url': reverse('index')}, request=request)

    def post(self, request: Request) -> Response:
        """
        Log In user
        """
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response_data = {'index_url': reverse('index'), 'msg': 'Successfull login'}
            return Response(data=response_data, status=status.HTTP_200_OK)
        return Response({'err': 'Invalid login'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
