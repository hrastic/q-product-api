"""
Views for the products APIs.
"""
from rest_framework import (
    viewsets,
    filters
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Product,
    Rating
)
from product import (
    serializers,
    paginations
)


class ProductViewSet(viewsets.ModelViewSet):
    """View for manage product APIs."""
    serializer_class = serializers.ProductSerializer
    pagination_class = paginations.StandardResultsSetPagination
    queryset = Product.objects.all().order_by('id')
    filter_backends = [filters.OrderingFilter]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class RatingViewSet(viewsets.ModelViewSet):
    """View for manage rating APIs."""
    serializer_class = serializers.RatingSerializer
    pagination_class = paginations.StandardResultsSetPagination
    queryset = Rating.objects.all().order_by('id')
    filter_backends = [filters.OrderingFilter]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
