from django.db import models
from accounts.models import User
from vendor.models import Vendor
from menu.models import FoodItem


# Create your models here.
class Payment(models.Model):
    PAYMENT_METHOD = (
        ('PayPal', 'PayPal'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=128)
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=128)
    amount = models.CharField(max_length=16)
    status = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id


class Order(models.Model):
    STATUS = (
        ('New', 'Chờ Xử Lý'),
        ('Accepted', 'Đã Chấp Nhận'),
        ('Completed', 'Đã Hoàn Thành'),
        ('Cancelled', 'Đã Hủy'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    vendors = models.ManyToManyField(Vendor, blank=True)
    order_number = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=16, blank=True)
    email = models.EmailField(max_length=64)
    address = models.CharField(max_length=256)
    country = models.CharField(max_length=16, blank=True)
    state = models.CharField(max_length=16, blank=True)
    city = models.CharField(max_length=64, blank=True)
    pin_code = models.CharField(max_length=16)
    total = models.FloatField()
    tax_data = models.JSONField(blank=True, help_text="Data format: {'tax_type':{'tax_percentage':'tax_amount'}}",
                                null=True)
    total_data = models.JSONField(blank=True, null=True)
    total_tax = models.FloatField()
    payment_method = models.CharField(max_length=32)
    status = models.CharField(max_length=16, choices=STATUS, default='New')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def customer_name(self):
        return f'{self.user.last_name} {self.user.first_name}'

    def order_placed_to(self):
        return ", ".join([str(i) for i in self.vendors.all()])

    def __str__(self):
        return self.order_number

    @classmethod
    def get_total_by_vendor(cls, order, user):
        vendor = Vendor.objects.get(user=user)
        subtotal = 0
        tax = 0
        print(order.tax_data)


class OrderedFood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.food_item.food_title
