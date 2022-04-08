from django.db.models import Count
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .filters import ProductFilter
from .pagination import ProductPagination
from .models import Product, Collection, OrderItem, Review
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = ProductPagination
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

    # Use context obj to provide additional data to a serializer (ProductSerializer). Providing the product_with_tax which is in the request obj coming.
    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        # Overide the destroy method by checking if there are order items in a particular product using the extracted product from the kwarg['pk] which the call has already been made in the default destory method by get_object()
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response(
                {'error': 'Product has one or more order items, so it can not be deleted'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response(
                {"error": "Collection has one or more products, so it can not be deleted"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    # Overide the get_queryset method the ReviewViewSet class so we can query the review objs under a particular product from the request url parameter(s) extracted from self.kwargs[''] which we do not have access to self in queryset
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk']).all()

    # Overide context obj and provide the additional data (product_id) to the serializer class
    def get_serializer_context(self):
        return {"product_id": self.kwargs['product_pk']}
