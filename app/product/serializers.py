"""
Serializers for product APIs
"""
from rest_framework import serializers

from core.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for products."""

    rating = serializers.FloatField(min_value=0, max_value=5)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'rating', 'updated_at']
        read_only_fields = ['id', 'updated_at']
