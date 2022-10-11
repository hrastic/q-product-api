"""
Tests for rating APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Product,
    Rating
)

from product.serializers import RatingSerializer


RATINGS_URL = reverse('product:rating-list')


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


def create_rating(user, product):
    """Create and return a new rating."""
    rating = Rating.objects.create(
        product=product,
        user=user,
        rating=5
    )
    return rating


class PublicRatingApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(RATINGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRatingApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ratings(self):
        """Test retrieving a list of ratings."""
        product1 = create_product()
        create_rating(self.user, product1)
        productAtts = {
            'name': 'Test Product2',
        }
        product2 = create_product(**productAtts)
        create_rating(self.user, product2)

        res = self.client.get(RATINGS_URL)

        ratings = Rating.objects.all().order_by('id')
        serializer = RatingSerializer(ratings, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_same_user_twice_unsuccessful(self):
        """Test that user can't rate the same product twice."""
        product = create_product()
        create_rating(self.user, product)
        payload = {
            'product': product,
            'user': self.user,
            'rating': 2
        }

        res = self.client.post(RATINGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
