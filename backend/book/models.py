from django.db import models
from user.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    STATUS_CHOICES = [
        ('available', '在售'),
        ('sold', '已售出'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    categories = models.ManyToManyField(Category, related_name='books')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
