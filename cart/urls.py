from django.urls import path
from .views import CartAPIView,CartItemAPIView

urlpatterns=[
    path('',CartAPIView.as_view(),name='cart'),
    path('<int:pk>/',CartItemAPIView.as_view(),name='cart-item'),
]