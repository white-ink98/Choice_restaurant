from datetime import date

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
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

        user = User.objects.create_user(username=username, password=password)
        return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)


class UserLogin(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key})


class RestaurantList(APIView):
    def get(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuList(APIView):
    def get(self, request):
        menus = Menu.objects.filter(date=date.today())
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeList(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VoteList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        employee, created = Employee.objects.get_or_create(user=user)
        menu_id = request.data.get('menu')

        try:
            menu = Menu.objects.get(id=menu_id, date=date.today())
        except Menu.DoesNotExist:
            return Response({'error': 'Menu not found for today'}, status=status.HTTP_404_NOT_FOUND)

        if Vote.objects.filter(employee=employee, menu=menu).exists():
            return Response({'error': 'You have already voted for this menu'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = VoteSerializer(data={'employee': employee.id, 'menu': menu.id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
