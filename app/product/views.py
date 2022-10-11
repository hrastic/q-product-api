"""
Views for the products APIs.
"""
from rest_framework import (
    viewsets,
    filters,
    status
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from django.db.models import Avg

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

    @action(detail=True, methods=['get'], url_path='store-average-rating')
    def store_average_rating(self, request, pk=None):
        """View for storing average rating on the product itself."""
        product = self.get_object()
        ratings = Rating.objects.filter(
            product=product
        ).aggregate(Avg('rating'))
        average_rating = round(ratings['rating__avg'], 2)
        serializer = serializers.ProductRatingSerializer(data={
            'name': product.name,
            'rating': average_rating,
            'price': product.price
        })
        if serializer.is_valid():
            product.rating = serializer.validated_data['rating']
            product.save()
            return Response({'status': 'Average rating set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    """View for manage rating APIs."""
    serializer_class = serializers.RatingSerializer
    pagination_class = paginations.StandardResultsSetPagination
    queryset = Rating.objects.all().order_by('id')
    filter_backends = [filters.OrderingFilter]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        """Return only details for ratings by authenticated user."""
        instance = self.get_object()
        if instance.user != self.request.user:
            return Response(
                {
                    "non_field_errors":
                        ["Unable to edit another users' review."]
                },
                status=status.HTTP_400_BAD_REQUEST)
        else:
            return super().update(request, *args, **kwargs)

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'update':
            return serializers.RatingDetailSerializer

        return self.serializer_class
