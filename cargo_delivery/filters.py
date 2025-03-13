import django_filters
from .models import Cargo, Truck
from geopy.distance import geodesic

class FilterCargo(django_filters.FilterSet):
    min_weight = django_filters.NumberFilter(field_name="weight", lookup_expr="gte")
    max_weight = django_filters.NumberFilter(field_name="weight", lookup_expr="lte")
    max_distance = django_filters.NumberFilter(method="filter_by_distance")

    def filter_by_distance(self, queryset, name, value):
        # Получаем все грузы
        cargos = queryset.all()
        # Получаем координаты всех машин
        trucks = Truck.objects.all()
        # Преобразуем в словарь координаты машин
        truck_coords = {truck.id: (truck.current_location.latitude, truck.current_location.longitude) for truck in trucks}
        filtered_cargos = []
        for cargo in cargos:
            cargo_coords = (cargo.pick_up.latitude, cargo.pick_up.longitude)
            # Для каждого груза находим ближайшую машину
            min_distance = float('inf')
            for truck_id, truck_coord in truck_coords.items():
                distance = geodesic(cargo_coords, truck_coord).km  # вычисляем расстояние в километрах
                if distance < min_distance:
                    min_distance = distance
            # Если расстояние меньше максимального, добавляем в результаты
            if min_distance <= value:
                filtered_cargos.append(cargo)

        return queryset.filter(id__in=[cargo.id for cargo in filtered_cargos])

    class Meta:
        model = Cargo
        fields = ['min_weight', 'max_weight', 'max_distance']

