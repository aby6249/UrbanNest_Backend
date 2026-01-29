from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    productName = serializers.CharField(source="product.name", read_only=True)
    image = serializers.URLField(source="product.image", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["productName", "image", "price", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "address",
            "payment_method",
            "total_amount",
            "status",
            "created_at",
            "items",
        ]
