"""
Serializers for product APIs
"""
from rest_framework import serializers

from core.models import (
    Product,
    Rating
)


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for products."""

    rating = serializers.FloatField(min_value=0, max_value=5)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'rating', 'updated_at']
        read_only_fields = ['id', 'updated_at']


class RatingSerializer(serializers.ModelSerializer):
    """Serializer for ratings."""

    class Meta:
        model = Rating
        fields = ['id', 'user', 'product', 'rating']
        read_only_fields = ['id']
