from django.db import models

from R4C.settings import NULLABLE
from customers.models import Customer


class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    robot_serial = models.CharField(max_length=5, **NULLABLE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

