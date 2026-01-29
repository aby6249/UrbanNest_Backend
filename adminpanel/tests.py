from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accountes.models import User
from products.models import Product
from orders.models import Order


class AdminAPITestCase(APITestCase):

    def setUp(self):
        """
        Runs before every test
        """

        
        self.admin = User.objects.create_user(
            email="admin1@gmail.com",
            password="admin123",
            is_staff=True,
            is_superuser=True
        )

    
        self.user = User.objects.create_user(
            email="user1@gmail.com",
            password="user123"
        )

   
        self.product = Product.objects.create(
            name="Sofa",
            new_price=20000,
            old_price=25000,
            category="living room",
            description="Test sofa",
            image="http://test.com/sofa.jpg",
            status="active"
        )

    
        self.order = Order.objects.create(
            user=self.user,
            total_amount=20000,
            status="Confirmed"
        )

        self.client.force_authenticate(user=self.admin)

 
    def test_admin_dashboard(self):
        url = "/api/admin/dashboard/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("users", response.data)
        self.assertIn("products", response.data)
        self.assertIn("orders", response.data)
        self.assertIn("revenue", response.data)

   
    def test_admin_orders_list(self):
        url = "/api/admin/orders/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

        order = response.data[0]

        self.assertIn("id", order)
        self.assertIn("user_id", order)
        self.assertIn("user_email", order)
        self.assertIn("user_name", order)
        self.assertIn("total_amount", order)
        self.assertIn("status", order)
        self.assertIn("created_at", order)


    def test_admin_users_list(self):
        url = "/api/admin/users/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)


    def test_admin_block_user(self):
        url = f"/api/admin/users/{self.user.id}/"
        response = self.client.patch(
            url,
            {"is_active": False},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

   
    def test_non_admin_cannot_access(self):
        self.client.force_authenticate(user=self.user)
        url = "/api/admin/dashboard/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
