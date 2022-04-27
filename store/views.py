from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    DjangoModelPermissions,
)
from rest_framework import status
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
)
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


from .filters import ProductFilter
from .pagination import ProductPagination
from .models import (
    Cart,
    CartItem,
    Customer,
    Order,
    Product,
    Collection,
    OrderItem,
    Review,
)
from .permissions import (
    CustomDjangoModelPermission,
    ViewCustomerHistoryPermission,
    IsAdminOrReadOnly,
)
from .serializers import (
    AddCartItemSerializer,
    CartItemSerializer,
    CartSerializer,
    CreateOrderSerializer,
    CustomerSerializer,
    OrderSerializer,
    ProductSerializer,
    CollectionSerializer,
    ReviewSerializer,
    UpdateCartItemSerializer,
)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = ProductPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ["title", "description"]
    ordering_fields = ["unit_price", "last_update"]

    def get_serializer_context(self):
        return {"request": self.request}

    def destroy(self, request, *args, **kwargs):

        if OrderItem.objects.filter(product_id=kwargs["pk"]).count() > 0:
            return Response(
                {
                    "error": "Product has one or more order items, so it can not be deleted"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs["pk"]).count() > 0:
            return Response(
                {
                    "error": "Collection has one or more products, so it can not be deleted"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["product_pk"]).all()

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}


class CartViewSet(
    CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, GenericViewSet
):
    queryset = Cart.objects.prefetch_related("items__product").all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}

    def get_queryset(self):
        return (
            CartItem.objects.filter(cart_id=self.kwargs["cart_pk"])
            .select_related("product")
            .all()
        )


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [CustomDjangoModelPermission]

    # def get_permissions(self):
    #     if self.request.method == "GET":
    #         return [AllowAny()]

    #     return [IsAuthenticated()]

    # Create a custom method called "me". We can make it available on the  instance/detail(yes pk) requests or collection/list(no pk) requests.
    # NOTE: All methods are called actions, so we can say here in this view we have the create action(made available via CreateModelMixins), update action(made available via UpdateModelMixin).
    @action(detail=False, methods=["GET", "PUT"], permission_classes=[IsAuthenticated])
    def me(self, request):
        (customer, _) = Customer.objects.get_or_create(user_id=request.user.id)
        if request.method == "GET":
            serializer = CustomerSerializer(instance=customer)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = CustomerSerializer(instance=customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response("Ok")


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return CreateOrderSerializer
        return OrderSerializer
    
    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.prefetch_related(
                "order_items", "order_items__product"
            ).all()

        (customer_id, _) = Customer.objects.only("id").get_or_create(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)
