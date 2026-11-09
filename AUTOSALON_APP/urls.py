from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
# Регистрируем 5 эндпоинтов (каждый ровно один раз!)
router.register(r'brands', views.BrandViewSet, basename='brand')
router.register(r'cars', views.CarViewSet, basename='car')
router.register(r'orders', views.OrderViewSet, basename='order')
router.register(r'employees', views.EmployeeViewSet, basename='employee')
router.register(r'test-drives', views.TestDriveViewSet, basename='testdrive')

urlpatterns = [
    # HTMX-эндпоинты — ВАЖНО: идут выше пустых путей
    path('get-cars/', views.car_list_element, name='car_list_element'),

    # API
    path('api/', include(router.urls)),

    # Главная страница — строго последней
    path('', views.catalog_page, name='catalog_page'),
]