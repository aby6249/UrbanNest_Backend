from rest_framework import serializers
from accountes.models import User
from products.models import Product
from orders.models import Order


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "second_name",
            "email",
            "is_active",
            "is_staff",
        ]


class AdminProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"



class DashboardSerializer(serializers.Serializer):
    user_count = serializers.IntegerField()
    product_count = serializers.IntegerField()
    order_count = serializers.IntegerField()
    revenue = serializers.IntegerField()
