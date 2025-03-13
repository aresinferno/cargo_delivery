from django.urls import include

from rest_framework.urls import path
from .views import CargoCreateAPIView, CargoListAPI, TruckUpdateAPiView, CargoUpdateAPIView, CargoDestroyAPIView, \
    CargoListAPIView, CargoDetailView, CargoFilterLisAPIView


urlpatterns = [
    path('api/cargo_create/', CargoCreateAPIView.as_view(), name='create_cargo'),
    path('api/cargo_list/', CargoListAPIView.as_view(), name='cargo_list'),
    path('api/truck_update/<int:id>', TruckUpdateAPiView.as_view(), name='truck_update'),
    path('api/cargo_update/<int:id>', CargoUpdateAPIView.as_view(), name='cargo_update'),
    path('api/cargo_destroy/<int:id>', CargoDestroyAPIView.as_view(), name='cargo_destroy'),
    path('api/cargo_list_distance/', CargoListAPI.as_view(), name='cargo_list_distance'),
    path('api/cargo_detail/<int:id>', CargoDetailView.as_view(), name='cargo_detail'),
    path('api/cargo_filter/', CargoFilterLisAPIView.as_view(), name='cargo')
]
