from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'brands', views.BrandViewSet, basename='brand')
router.register(r'cars', views.CarViewSet, basename='car')
router.register(r'orders', views.OrderViewSet, basename='order')
router.register(r'employees', views.EmployeeViewSet, basename='employee')
router.register(r'test-drives', views.TestDriveViewSet, basename='testdrive')

urlpatterns = [
    # --- ГЛАВНАЯ СТРАНИЦА И HTMX ---
    path('get-cars/', views.car_list_element, name='car_list_element'),
    path('', views.catalog_page, name='catalog_page'),
    # -------------------------------

    # API
    path('api/v1/cars/', views.api_cars_list, name='api_v1_cars'),
    path('api/v1/orders/', views.api_create_order, name='api_v1_orders'),
    path('api/', include(router.urls)),
]