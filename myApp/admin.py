from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Produce, Order, SalesData, PageView

admin.site.register(Produce)
admin.site.register(Order)
admin.site.register(SalesData)
admin.site.register(PageView)
