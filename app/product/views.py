"""
Views for the products APIs.
"""
from rest_framework import (
    viewsets,
    filters
)

from core.models import Product
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
