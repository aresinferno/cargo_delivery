from rest_framework import serializers
from .models import *


class LocationSerializer(serializers.ModelSerializer):
    model = Location
    fields = '__all__'

class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['pick_up', 'delivery', 'weight', 'description']



class CargoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['weight', 'description']


class CargoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['id', 'pick_up', 'delivery', 'weight', 'description']


class CargoCreateSerializer(serializers.ModelSerializer):
    pickup_zip_code = serializers.CharField(write_only=True)
    delivery_zip_code = serializers.CharField(write_only=True)
    weight = serializers.FloatField(write_only=True)
    description = serializers.CharField(write_only=True)

    class Meta:
        model = Cargo
        fields = ['pickup_zip_code', 'delivery_zip_code', 'weight', 'description', 'pick_up', 'delivery']
        read_only_fields = ['pick_up', 'delivery']

    def create(self, validated_data):
        pickup_zip_code = validated_data.pop('pickup_zip_code')
        delivery_zip_code = validated_data.pop('delivery_zip_code')
        weight = validated_data.pop('weight')
        description = validated_data.pop('description')
        try:
            pick_up = Location.objects.get(zip_code=pickup_zip_code)
            delivery = Location.objects.get(zip_code=delivery_zip_code)
        except Location.DoesNotExist:
            raise serializers.ValidationError('One or both ZIP codes are invalid')

        cargo = Cargo.objects.create(
            pick_up=pick_up,
            delivery=delivery,
            weight=weight,
            description=description
        )
        return cargo

class TruckSerializer(serializers.ModelSerializer):
    current_location = serializers.CharField()
    class Meta:
        model = Truck
        fields = ['current_location']
    def create(self, validated_data):
        current_location_zip = validated_data.pop('current_location')
        try:
            current_location = Location.objects.get(zip_code=current_location_zip)
        except Location.DoesNotExist:
            raise serializers.ValidationError('One or both ZIP codes are invalid')

        truck = Truck.objects.create(
            current_location=current_location,
            **validated_data
        )

        return truck

