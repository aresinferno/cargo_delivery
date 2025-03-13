from django.db import models

from django.db import models
import random, string

class Location(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.IntegerField(unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

class Cargo(models.Model):
    pick_up = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='pickup_cargos')
    delivery = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='delivery_cargos')
    weight = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return f'{self.pick_up}, {self.delivery}, {self.weight}, {self.description}'


class Truck(models.Model):
    truck_number = models.CharField(max_length=5)
    current_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    lifting_capacity = models.FloatField()

    def add_number(self, truck_number):
        if not truck_number:
            truck_number = f'{random.randint(1000, 9999)}{random.choice(string.ascii_uppercase)}'
        return truck_number

# Create your models here.


# Create your models here.

# Create your models here.
