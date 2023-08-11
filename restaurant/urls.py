from django.urls import path

from .views import (EmployeeList, MenuList, RestaurantList, UserLogin,
                    UserRegistration, VoteList)

urlpatterns = [
    path('registration/', UserRegistration.as_view(), name='user-register'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('restaurants/', RestaurantList.as_view(), name='restaurant-list'),
    path('menus/', MenuList.as_view(), name='menu-list'),
    path('employees/', EmployeeList.as_view(), name='employee-list'),
    path('votes/', VoteList.as_view(), name='vote-list'),
]
