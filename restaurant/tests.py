from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Employee, Menu, Vote
from .serializers import MenuSerializer, RestaurantSerializer


class UserRegistrationTest(TestCase):
    def test_user_registration(self):
        client = APIClient()
        response = client.post(
            reverse('user-registration'),
            {'username': 'testuser', 'password': 'testpassword'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')


class UserLoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_user_login(self):
        client = APIClient()
        response = client.post(
            reverse('user-login'),
            {'username': 'testuser', 'password': 'testpassword'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)


class VoteListTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.menu = Menu.objects.create(name='Menu 1', date=date.today())
        self.employee = Employee.objects.create(user=self.user)

    def test_create_vote(self):
        response = self.client.post(
            reverse('vote-list'),
            {'menu': self.menu.id},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vote.objects.count(), 1)

    def test_create_duplicate_vote(self):
        Vote.objects.create(employee=self.employee, menu=self.menu)
        response = self.client.post(
            reverse('vote-list'),
            {'menu': self.menu.id},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_vote_for_nonexistent_menu(self):
        response = self.client.post(
            reverse('vote-list'),
            {'menu': 999},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MenuListTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_menus(self):
        response = self.client.get(reverse('menu-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RestaurantSerializerTest(TestCase):
    def test_serialize_restaurant(self):
        restaurant_data = {'name': 'Test Restaurant', 'location': 'Test Location'}
        serializer = RestaurantSerializer(data=restaurant_data)
        self.assertTrue(serializer.is_valid())
        serialized_data = serializer.data
        self.assertEqual(serialized_data['name'], 'Test Restaurant')
        self.assertEqual(serialized_data['location'], 'Test Location')


class MenuSerializerTest(TestCase):
    def test_serialize_menu(self):
        menu_data = {'name': 'Test Menu', 'date': '2023-08-08'}
        serializer = MenuSerializer(data=menu_data)
        self.assertTrue(serializer.is_valid())
        serialized_data = serializer.data
        self.assertEqual(serialized_data['name'], 'Test Menu')
        self.assertEqual(serialized_data['date'], '2023-08-08')
