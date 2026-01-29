from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import CartItem
from .serializers import CartItemSerializer
from products.models import Product



class CartAPIView(APIView):
    permission_classes=[IsAuthenticated]


    def get(self,request):
        cart_items=CartItem.objects.filter(user=request.user)
        serializer=CartItemSerializer(cart_items,many=True)
        return Response(serializer.data)
    

    def post(self,request):
        product_id=request.data.get('productId')
        quantity=int(request.data.get('quantity',1))


        try:
            product=Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error":"Product not found"},status=status.HTTP_400_BAD_REQUEST)
        

        cart_item,created = CartItem.objects.get_or_create(
            user=request.user,
            product=product
        )

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()


        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    


class CartItemAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def patch(self,request,pk):
        try:
            cart_item = CartItem.objects.get(pk=pk,user=request.user)
        except CartItem.DoesNotExist:
            return Response(status=404)
        
        quantity = int(request.data.get('quantity', 1))
        if quantity<1:
            return Response({"error":"Quantity must be at least 1"},status=status.HTTP_404_NOT_FOUND)
        

        cart_item.quantity=quantity
        cart_item.save()
        return Response(CartItemSerializer(cart_item).data)
    

    def delete(self,request,pk):
        try:
            cart_item=CartItem.objects.get(pk=pk,user=request.user)
        except CartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
