from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum

from accountes.models import User
from products.models import Product
from orders.models import Order

from .serializers import AdminUserSerializer,AdminProductSerializer
from .permissions import IsAdmin



class AdminDashboardAPIView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({
            "users": User.objects.count(),
            "products": Product.objects.filter(status="active").count(),
            "orders": Order.objects.count(),
            "revenue": Order.objects.aggregate(
                total=Sum("total_amount")
            )["total"] or 0
        })



class AdminUserListAPIView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        users = User.objects.filter(is_superuser=False)
        serializer = AdminUserSerializer(users, many=True)
        return Response(serializer.data)


class AdminUserUpdateAPIView(APIView):
    permission_classes = [IsAdmin]

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=404)

        if "is_active" in request.data:
            user.is_active = request.data["is_active"]

        # if "is_staff" in request.data:
        #     user.is_staff = request.data["is_staff"]

        user.save()
        return Response(AdminUserSerializer(user).data)




class AdminProductListCreateAPIView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        products = Product.objects.all()
        serializer = AdminProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AdminProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)




class AdminProductUpdateAPIView(APIView):
    permission_classes = [IsAdmin]

    def patch(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=404)

        if "status" in request.data:
            product.status = request.data["status"]

        product.save()
        return Response(AdminProductSerializer(product).data)



class AdminOrderListAPIView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        orders = Order.objects.select_related("user").prefetch_related("items__product").order_by("-id")

        data = []
        for order in orders:
            data.append({
                "id": order.id,
                "user_id": order.user.id if order.user else None,
                "user_name": f"{order.user.first_name} {order.user.second_name}" if order.user else "Guest",
                "user_email": order.user.email if order.user else "Guest",
                "products": [
                    {
                        "id": item.product.id,
                        "name": item.product.name,
                        "qty": item.quantity
                    }
                    for item in order.items.all()
                ],
                "total_amount": order.total_amount,
                "status": order.status,
                "created_at": order.created_at,
            })

        return Response(data)
