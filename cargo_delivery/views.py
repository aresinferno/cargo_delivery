import django_filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .serializers import CargoSerializer, CargoCreateSerializer, TruckSerializer, CargoUpdateSerializer, \
    CargoDetailSerializer
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from .models import *
from geopy.distance import geodesic
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .filters import FilterCargo


class CargoListAPIView(ListAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer


class TruckUpdateAPiView(UpdateAPIView):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer
    lookup_field = 'id'


class CargoUpdateAPIView(UpdateAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoUpdateSerializer
    lookup_field = 'id'


class CargoDestroyAPIView(DestroyAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer
    lookup_field = 'id'


class CargoListAPI(APIView):
    def get(self, request):
        cargo_list = []
        for cargo in Cargo.objects.all():
            nearest_trucks = []
            cargo_location = (cargo.pick_up.latitude, cargo.pick_up.longitude)
            for truck in Truck.objects.all():
                if truck.current_location:
                    truck_location = (truck.current_location.latitude, truck.current_location.longitude)
                    distance = geodesic(cargo_location, truck_location).miles
                    if distance <= 450:
                        nearest_trucks.append({"truck_id": truck.id, "distance": distance})
            cargo_list.append({
                "cargo_id": cargo.id,
                "nearest_trucks": nearest_trucks
            })
        return Response(cargo_list, status=status.HTTP_200_OK)


class CargoCreateAPIView(APIView):
    @swagger_auto_schema(request_body=CargoCreateSerializer)
    def post(self, request):
        response_serializer = []
        serializer = CargoCreateSerializer(data=request.data)
        if serializer.is_valid():
            response_serializer.append({
                'pick_up': serializer.validated_data.get('pick_up'),
                'delivery': serializer.validated_data.get('delivery'),
                'weight': serializer.validated_data.get('weight'),
                'description': serializer.validated_data.get('description')
            })
            serializer.save()

            return Response(response_serializer, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CargoDetailAPIView(APIView):
#     def get(self, request):
#         self.cargo = request.data.get('')
#         responce_data = []
#         for cargo in Cargo.objects.all():
#             truck_distance = []
#             cargo_location = (cargo.pick_up.latitude, cargo.pick_up.longitude)
#             for truck in Truck.objects.all():
#                 truck_location = (truck.current_location.latitude, truck.current_location.longitude)
#                 distance = geodesic(cargo_location.)

class CargoDetailView(RetrieveAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoDetailSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        cargo = self.get_object()  # Получаем объект груза
        trucks = Truck.objects.all()  # Получаем все машины

        # Координаты груза
        cargo_location = (cargo.pick_up.latitude, cargo.pick_up.longitude)

        # Считаем расстояние от всех машин до груза
        trucks_info = [
            {
                "truck_number": truck.truck_number,
                "distance_miles": round(
                    geodesic(cargo_location, (truck.current_location.latitude, truck.current_location.longitude)).miles,
                    2)
            }
            for truck in trucks
        ]

        # Сортируем по расстоянию (по возрастанию)
        trucks_info.sort(key=lambda x: x["distance_miles"])

        # Формируем ответ
        data = {
            "id": cargo.id,
            "pick_up": {
                "city": cargo.pick_up.city,
                "state": cargo.pick_up.state,
                "zip": cargo.pick_up.zip_code
            },
            "delivery": {
                "city": cargo.delivery.city,
                "state": cargo.delivery.state,
                "zip": cargo.delivery.zip_code
            },
            "weight": cargo.weight,
            "description": cargo.description,
            "trucks": trucks_info  # Добавляем список машин с расстоянием
        }

        return Response(data)


class CargoFilterLisAPIView(ListAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FilterCargo
