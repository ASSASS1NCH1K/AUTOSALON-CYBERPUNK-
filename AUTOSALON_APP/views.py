from django.shortcuts import render
from django.views.decorators.http import require_GET
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Brand, Car, Order, Employee, TestDrive
from .serializers import (
    BrandSerializer, CarSerializer, OrderSerializer, EmployeeSerializer, TestDriveSerializer
)

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.select_related('brand').all()
    serializer_class = CarSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('car', 'manager').all()
    serializer_class = OrderSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class TestDriveViewSet(viewsets.ModelViewSet):
    queryset = TestDrive.objects.select_related('car').all()
    serializer_class = TestDriveSerializer

def catalog_page(request):
    cars = Car.objects.select_related('brand').all()
    return render(request, 'autosalon/catalog.html', {'cars': cars})

@require_GET
def car_list_element(request):
    cars = Car.objects.select_related('brand').all()
    return render(request, 'autosalon/car_cards.html', {'cars': cars})

@api_view(['GET'])
def api_cars_list(request):
    cars = Car.objects.select_related('brand').all()
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def api_create_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)