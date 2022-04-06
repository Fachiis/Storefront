from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    # Extra context provided to the serializer class.
    def get_serializer_context(self):
        return {'request': self.request}


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Customize the delete method by overriding the delete method the RetrieveUpdateDestroyAPIView.delete()
    def delete(self, request, pk, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        if product.order_items.count() > 0:  # type: ignore
            return Response(
                {'error': 'Product has one or more order items, so it can not be deleted'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer


class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def delete(self, request, pk, **kwargs):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:  # type: ignore
            return Response(
                {"error": "Collection has one or more products, so it can not be deleted"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
