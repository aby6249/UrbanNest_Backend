from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import CartItem

class OrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        address = request.data.get("address")
        payment_method = request.data.get("paymentMethod")
    
        if not address or not payment_method:
            return Response(
                {"error": "Address and payment method required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_items = CartItem.objects.filter(user=request.user)

        if not cart_items.exists():
            return Response(
                {"error": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        total = sum(
            item.product.new_price * item.quantity for item in cart_items
        ) + 100  

        order = Order.objects.create(
            user=request.user,
            address=address,
            payment_method=payment_method,
            total_amount=total,
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.new_price,
            )


        cart_items.delete()

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )
