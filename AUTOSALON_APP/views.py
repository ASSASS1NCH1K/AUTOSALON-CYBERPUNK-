from django.shortcuts import render
from django.views.decorators.http import require_GET
from rest_framework import viewsets

from .models import Brand, Car, Order, Employee, TestDrive
from .serializers import (
    BrandSerializer, 
    CarSerializer, 
    OrderSerializer, 
    EmployeeSerializer, 
    TestDriveSerializer
)


# --- СТАРЫЕ VIEWSETS (ВОССТАНОВЛЕНЫ) ---
class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.select_related('brand').all()
    serializer_class = CarSerializer


# --- НОВЫЕ И ОБНОВЛЕННЫЕ VIEWSETS ---
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('car', 'manager').all()
    serializer_class = OrderSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class TestDriveViewSet(viewsets.ModelViewSet):
    queryset = TestDrive.objects.select_related('car').all()
    serializer_class = TestDriveSerializer


# --- ФУНКЦИИ ДЛЯ ФРОНТЕНДА ---
def catalog_page(request):
    cars = Car.objects.select_related('brand').all()
    return render(request, 'autosalon/catalog.html', {'cars': cars})


@require_GET
def car_list_element(request):
    cars = Car.objects.select_related('brand').all()
    return render(request, 'autosalon/car_cards.html', {'cars': cars})