from rest_framework import serializers
from .models import Order, Cart

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'ordered_at']
