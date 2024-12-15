from django.db import models
from user.models import User

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
    categories = models.ManyToManyField('Category', through='BookCategory')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cover_url = models.URLField(blank=True, null=True)  # 新增封面字段

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=255)

class BookCategory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
