from django.contrib import admin
from .models import Brand, Car, Order, Employee, TestDrive


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country', 'created_at')
    search_fields = ('name', 'country')
    list_filter = ('country',)
    ordering = ('name',)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'model_name', 'year', 'color', 'price', 'status', 'created_at')
    list_editable = ('price', 'status')
    list_filter = ('status', 'brand', 'year', 'color')
    search_fields = ('brand__name', 'model_name', 'color', 'description')
    list_select_related = ('brand',)
    autocomplete_fields = ('brand',)
    ordering = ('-created_at',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'position', 'phone')
    search_fields = ('full_name', 'position')
    list_filter = ('position',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'car', 'customer_name', 'customer_phone', 'manager', 'created_at')
    list_filter = ('manager', 'created_at', 'car__brand')
    search_fields = ('customer_name', 'customer_phone', 'car__model_name', 'car__brand__name')
    list_select_related = ('car', 'car__brand', 'manager')
    autocomplete_fields = ('car', 'manager')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(TestDrive)
class TestDriveAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_name', 'car', 'date_time', 'status')
    list_filter = ('status', 'date_time')
    list_editable = ('status',)
    search_fields = ('client_name', 'client_phone')
    autocomplete_fields = ('car',)