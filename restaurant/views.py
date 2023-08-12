from datetime import date

from django.contrib.auth.models import User
from rest_framework import status, serializers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Employee, Menu, Restaurant, Vote
from .serializers import (EmployeeSerializer, MenuSerializer,
                          RestaurantSerializer, VoteSerializer)


class UserRegistration(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({
                'error': 'Username already exists. Please choose a different username.'
            }, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)


class UserLogin(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key})


class RestaurantList(ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class MenuList(ListCreateAPIView):
    queryset = Menu.objects.filter(date=date.today())
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class EmployeeList(ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class VoteList(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VoteSerializer

    def perform_create(self, serializer):
        user = self.request.user
        employee, created = Employee.objects.get_or_create(user=user)
        menu_id = self.request.data.get('menu')

        try:
            menu = Menu.objects.get(id=menu_id, date=date.today())
        except Menu.DoesNotExist:
            raise serializers.ValidationError({'error': 'Menu not found for today'})

        if Vote.objects.filter(employee=employee, menu=menu).exists():
            raise serializers.ValidationError({'error': 'You have already voted for this menu'})

        serializer.save(employee=employee, menu=menu)
