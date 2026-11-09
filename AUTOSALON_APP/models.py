from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Марка')
    country = models.CharField(max_length=100, blank=True, verbose_name='Страна')
    logo = models.ImageField(upload_to='brands/', blank=True, null=True, verbose_name='Логотип')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'
        ordering = ['name']

    def __str__(self):
        return self.name

class Car(models.Model):
    STATUS_AVAILABLE = 'available'
    STATUS_RESERVED = 'reserved'
    STATUS_SOLD = 'sold'

    STATUS_CHOICES = [
        (STATUS_AVAILABLE, 'В наличии'),
        (STATUS_RESERVED, 'Забронирован'),
        (STATUS_SOLD, 'Продан'),
    ]

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='cars', verbose_name='Марка')
    model_name = models.CharField(max_length=150, verbose_name='Модель')
    year = models.PositiveIntegerField(verbose_name='Год выпуска')
    color = models.CharField(max_length=50, verbose_name='Цвет')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена, ₽')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_AVAILABLE, verbose_name='Статус')
    image = models.ImageField(upload_to='cars/', blank=True, null=True, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.brand.name} {self.model_name} ({self.year})'

class Employee(models.Model):
    full_name = models.CharField(max_length=150, verbose_name='ФИО')
    position = models.CharField(max_length=100, verbose_name='Должность')
    phone = models.CharField(max_length=30, blank=True, verbose_name='Телефон')
    photo = models.ImageField(upload_to='employees/', blank=True, null=True, verbose_name='Фото')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['full_name']

    def __str__(self):
        return f'{self.full_name} ({self.position})'

class Order(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='orders', verbose_name='Автомобиль')
    customer_name = models.CharField(max_length=150, verbose_name='Имя клиента')
    customer_phone = models.CharField(max_length=30, verbose_name='Телефон')
    manager = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Менеджер')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заявка #{self.pk} — {self.customer_name} → {self.car}'

class TestDrive(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('confirmed', 'Подтвержден'),
        ('cancelled', 'Отменен'),
    ]

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='test_drives', verbose_name='Автомобиль')
    client_name = models.CharField(max_length=150, verbose_name='Имя клиента')
    client_phone = models.CharField(max_length=30, verbose_name='Телефон')
    date_time = models.DateTimeField(verbose_name='Дата и время')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')

    class Meta:
        verbose_name = 'Тест-драйв'
        verbose_name_plural = 'Тест-драйвы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Тест-драйв: {self.client_name} на {self.car}'