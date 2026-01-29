from rest_framework import serializers
from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    productId=serializers.IntegerField(source='product.id',read_only=True)
    productName=serializers.CharField(source='product.name',read_only=True)
    productPrice=serializers.IntegerField(source='product.new_price',read_only=True)
    image = serializers.URLField(source='product.image', read_only=True)



    class Meta:
        model=CartItem
        fields=[
            'id',
            'productId',
            'productName',
            'productPrice',
            'image',
            'quantity',
        ]