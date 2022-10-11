"""
Tests for product APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Product

from product.serializers import ProductSerializer


PRODUCTS_URL = reverse('product:product-list')


def detail_url(product_id):
    """Create and return a product detail URL."""
    return reverse('product:product-detail', args=[product_id])


def create_product(**params):
    """Create and return a new product."""
    defaults = {
        'name': 'Test Product',
        'price': Decimal('2.50'),
        'rating': 5
    }
    defaults.update(params)

    product = Product.objects.create(**defaults)
    return product


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicProductApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(PRODUCTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProductApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_products(self):
        """Test retrieving a list of products."""
        create_product()
        productAttributes = {
            'name': 'Test Product2',
        }
        create_product(**productAttributes)

        res = self.client.get(PRODUCTS_URL)

        products = Product.objects.all().order_by('id')
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_get_product_detail(self):
        """Test get product detail."""
        product = create_product()

        url = detail_url(product.id)
        res = self.client.get(url)

        serializer = ProductSerializer(product)
        self.assertEqual(res.data, serializer.data)

    def test_create_product(self):
        """Test creating a product."""
        payload = {
            'name': 'Test Product',
            'price': Decimal('2.50'),
            'rating': 5
        }
        res = self.client.post(PRODUCTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(product, k), v)

    def test_partial_update(self):
        """Test partial update of a product."""
        original_price = Decimal('120.45')
        original_rating = 4.8
        product = create_product(
            name='Test Product',
            price=original_price,
            rating=original_rating
        )
        payload = {'name': 'New product title'}
        url = detail_url(product.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.name, payload['name'])
        self.assertEqual(product.price, original_price)
        self.assertEqual(product.rating, original_rating)

    def test_full_update(self):
        """Test full update of a product."""
        product = create_product(
            name='Test Product',
            price=Decimal('120.45'),
            rating=4.8
        )

        payload = {
            'name': 'New recipe title',
            'price': Decimal('125.25'),
            'rating': 4.2
        }
        url = detail_url(product.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(product, k), v)

    def test_updating_name_into_existing_one_unsuccessful(self):
        """
        Test that updating name of a product into already existing one is
        unsuccessful.
        """
        create_product(
            name='Test Product',
            price=Decimal('100.00'),
            rating=4
        )
        product2 = create_product(
            name='Test Product2',
            price=Decimal('115.50'),
            rating=5
        )

        payload = {'name': 'Test Product'}
        url = detail_url(product2.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(product2.name, payload['name'])

    def test_delete_product(self):
        """Test deleting a product successful."""
        product = create_product()

        url = detail_url(product.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=product.id).exists())
