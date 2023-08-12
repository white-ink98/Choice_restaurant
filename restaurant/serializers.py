from rest_framework import serializers

from .models import Employee, Menu, Restaurant, Vote


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'

    def validate(self, data):
        # already voted for this menu
        employee = data['employee']
        menu = data['menu']

        if Vote.objects.filter(employee=employee, menu=menu).exists():
            raise serializers.ValidationError('You have already voted for this menu.')

        return data


class EmployeeWithVotesSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'
