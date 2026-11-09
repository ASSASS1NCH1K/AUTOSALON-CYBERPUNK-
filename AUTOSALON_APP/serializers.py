from rest_framework import serializers
from .models import Brand, Car, Order, Employee, TestDrive

# Твои старые сериализаторы (обрати внимание: без буквы S на конце!)
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'country', 'logo', 'created_at']
        read_only_fields = ['id', 'created_at']

class CarSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Car
        fields = [
            'id', 'brand', 'brand_name', 'model_name', 'year', 'color',
            'price', 'status', 'status_display', 'image', 'description', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

# НОВЫЕ сериализаторы
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    car_info = CarSerializer(source='car', read_only=True)
    manager_info = EmployeeSerializer(source='manager', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'car', 'car_info', 'manager', 'manager_info', 'customer_name', 'customer_phone', 'created_at']

    def validate(self, attrs):
        car = attrs.get('car')
        if car and car.status == Car.STATUS_SOLD:
            raise serializers.ValidationError({'car': 'Этот автомобиль уже продан, заявка невозможна.'})
        if car and car.status == Car.STATUS_RESERVED:
            raise serializers.ValidationError({'car': 'Автомобиль уже забронирован.'})
        return attrs

class TestDriveSerializer(serializers.ModelSerializer):
    car_info = CarSerializer(source='car', read_only=True)

    class Meta:
        model = TestDrive
        fields = ['id', 'car', 'car_info', 'client_name', 'client_phone', 'date_time', 'status', 'created_at']