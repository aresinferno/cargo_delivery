import random
from celery import shared_task
from .models import Truck

@shared_task
def update_truck_locations():
    for truck in Truck.objects.all():
        truck.current_location.latitude += random.uniform(-0.1, 0.1)
        truck.current_location.longitude += random.uniform(-0.1, 0.1)
        truck.current_location.save()
    return "Locations updated"

