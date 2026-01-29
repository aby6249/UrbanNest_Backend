from django.db import models

class Product(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    CATEGORY_CHOICES = (
        ('living room', 'Living Room'),
        ('bedroom', 'Bedroom'),
        ('dining room', 'Dining Room'),
        ('lamps & lighting', 'Lamps & Lighting'),
    )

    name = models.CharField(max_length=200)
    image = models.URLField()
    new_price = models.IntegerField()
    old_price = models.IntegerField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
