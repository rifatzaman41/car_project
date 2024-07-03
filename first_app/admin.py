from django.contrib import admin
from .models import Car, Order
from django import template

register = template.Library()
@register.simple_tag
def buy_now():
    return "Buy Now"
admin.site.register(Car)
admin.site.register(Order)
