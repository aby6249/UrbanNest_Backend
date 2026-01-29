from django.urls import path
from .views import AdminDashboardAPIView,AdminUserListAPIView,AdminUserUpdateAPIView,AdminProductListCreateAPIView,AdminProductUpdateAPIView,AdminOrderListAPIView

urlpatterns = [
    path("dashboard/", AdminDashboardAPIView.as_view()),
    path("users/", AdminUserListAPIView.as_view()),
    path("users/<int:pk>/", AdminUserUpdateAPIView.as_view()),
    path("orders/", AdminOrderListAPIView.as_view()),
    path("products/", AdminProductListCreateAPIView.as_view()),
    path("products/<int:pk>/", AdminProductUpdateAPIView.as_view()),
]
