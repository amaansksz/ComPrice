from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    image = models.ImageField()
    link = models.URLField()
    def __str__(self):
        return self.name
