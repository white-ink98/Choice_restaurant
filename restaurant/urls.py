from django.urls import path

from .views import EmployeeList, MenuList, RestaurantList, VoteList

urlpatterns = [
    path('restaurants/', RestaurantList.as_view(), name='restaurant-list'),
    path('menus/', MenuList.as_view(), name='menu-list'),
    path('employees/', EmployeeList.as_view(), name='employee-list'),
    path('votes/', VoteList.as_view(), name='vote-list'),
]
