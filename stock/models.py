from django.db import models
from ckeditor.fields import RichTextField

# stock product
class Product(models.Model):
    product_name = models.CharField(max_length=128)
    product_detail = RichTextField()
    product_barcode = models.CharField(max_length=13)
    product_qty = models.IntegerField()
    product_price = models.DecimalField(max_digits=7, decimal_places=2)
    product_image = models.CharField(max_length=128)
    product_status = models.IntegerField()

    def __str__(self):
        return self.product_name


# DataPoint for chart plot
class DataPoint(models.Model):
    x_value = models.IntegerField()
    y_value = models.FloatField()

    def __str__(self):
        return str(self.x_value)

# Person model
class Person(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.name
