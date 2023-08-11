from django.contrib import admin

from .models import Employee, Menu, Restaurant, Vote


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    fields = ('name', 'address')


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'date', 'items')
    list_filter = ('restaurant', 'date')
    fields = ('restaurant', 'date', 'items')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'version')
    fields = ('user', 'version')


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('employee', 'menu', 'voted_at')
    list_filter = ('employee', 'menu', 'voted_at')
    fields = ('employee', 'menu', 'voted_at')
