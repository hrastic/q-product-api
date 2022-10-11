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


class ProductRatingSerializer(ProductSerializer):
    """Serializer for product rating."""

    rating = serializers.FloatField(min_value=0, max_value=5)

    class Meta(ProductSerializer.Meta):
        model = Product
        read_only_fields = \
            ProductSerializer.Meta.read_only_fields + \
            ['name', 'price']


class RatingSerializer(serializers.ModelSerializer):
    """Serializer for ratings."""

    rating = serializers.IntegerField(min_value=0, max_value=5)

    class Meta:
        model = Rating
        fields = ['id', 'user', 'product', 'rating']
        read_only_fields = ['id']


class RatingDetailSerializer(RatingSerializer):
    """Serializer for ratings detail."""

    class Meta(RatingSerializer.Meta):
        model = Rating
        read_only_fields = \
            RatingSerializer.Meta.read_only_fields + \
            ['user', 'product']
