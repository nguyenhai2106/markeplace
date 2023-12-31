from django.db import models
from vendor.models import Vendor
from tabnanny import verbose


# Create your models here.
class Category(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=128)
    description = models.TextField(max_length=256, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        unique_together = ('vendor', 'category_name', 'slug')

    def clean(self):
        self.category_name = self.category_name.capitalize()

    def __str__(self):
        return self.category_name

    def short_description(self):
        return self.description.split(".")[0] + '.'


class FoodItem(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='fooditems')
    food_title = models.CharField(max_length=64)
    slug = models.SlugField(max_length=128, unique=True)
    description = models.TextField(max_length=256, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='foodimages')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.food_title
    def short_description(self):
        return self.description.split(".")[0] + '.'
