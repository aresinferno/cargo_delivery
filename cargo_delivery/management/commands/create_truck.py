import random
from string import ascii_uppercase
from django.core.management.base import BaseCommand
from cargo_delivery.models import Truck, Location

class Command(BaseCommand):
    help = "Создает 20 случайных грузовиков"

    def handle(self, *args, **kwargs):
        locations = list(Location.objects.all())
        trucks = []
        for _ in range(20):
            truck_number = f'{random.randint(1000, 9999)}{random.choice(ascii_uppercase)}'
            current_location = random.choice(locations) if locations else None
            lifting_capacity = random.randint(1, 1000)
            truck = Truck(truck_number=truck_number, current_location=current_location, lifting_capacity=lifting_capacity)
            trucks.append(truck)
        Truck.objects.bulk_create(trucks)
        self.stdout.write(self.style.SUCCESS("20 trucks created successfully"))
