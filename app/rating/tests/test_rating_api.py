"""
Tests for rating APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Rating

from product.serializers import RatingSerializer


RATINGS_URL = reverse('rating:rating-list')
RATE_URL = reverse('product:rate-product')


def rate_product_url(product_id):
    """Create and return product rating URL."""
    return reverse(RATE_URL, args=[product_id])


class PublicRatingApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(RATINGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
