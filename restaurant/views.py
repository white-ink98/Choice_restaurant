from datetime import date

# from django.views.generic import ListView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from restaurant.api.serializers import (EmployeeSerializer, MenuSerializer,
                                        RestaurantSerializer, VoteSerializer)

from .models import Employee, Menu, Restaurant, Vote


# class RestaurantView(ListView):
#     model = Restaurant
#     queryset = Restaurant.objects.filter(draft=False)


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
        employee = request.user.employee
        menu_id = request.data.get('menu')
        try:
            menu = Menu.objects.get(id=menu_id)
        except Menu.DoesNotExist:
            return Response({'error': 'Menu not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the employee has already voted for this menu
        if Vote.objects.filter(employee=employee, menu=menu).exists():
            return Response({'error': 'You have already voted for this menu'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = VoteSerializer(data={'employee': employee.id, 'menu': menu.id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
