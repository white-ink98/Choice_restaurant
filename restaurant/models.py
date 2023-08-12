from django.contrib.auth.models import User
from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField()
    items = models.TextField()


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    version_choices = (
        ('v1', 'Version 1'),
        ('v2', 'Version 2'),
    )
    version = models.CharField(max_length=10, choices=version_choices)  # mobile app version

    def __str__(self):
        return self.user.username


class Vote(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'menu')
