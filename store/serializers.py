from decimal import Decimal
from django.db import transaction
from rest_framework import serializers

from .signals import order_created
from .models import (
    Cart,
    CartItem,
    Customer,
    Order,
    OrderItem,
    Product,
    Collection,
    Review,
)


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title", "products_count"]

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "inventory",
            "unit_price",
            "price_with_tax",
            "collection",
        ]

    price_with_tax = serializers.SerializerMethodField(
        method_name="calculate_price_with_tax"
    )

    def calculate_price_with_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "unit_price"]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "date", "name", "description"]

    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id=product_id, **validated_data)


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(
        method_name="get_total_price", read_only=True
    )

    def get_total_price(self, cart_item: CartItem):
        return cart_item.product.unit_price * cart_item.quantity

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                f"Product with ID {value} does not exist."
            )
        return value

    class Meta:
        model = CartItem
        fields = ["id", "product_id", "quantity"]

    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"]
        quantity = self._validated_data["quantity"]
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data
            )

        return self.instance


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(
        method_name="get_total_price", read_only=True
    )

    def get_total_price(self, cart: Cart):
        return sum(item.quantity * item.product.unit_price for item in cart.items.all())

    class Meta:
        model = Cart
        fields = ["id", "items", "total_price"]


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ["id", "user_id", "birth_date", "phone", "membership"]


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "unit_price", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_id",
            "placed_at",
            "payment_status",
            "order_items",
        ]


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["payment_status"]


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    # To create a custom validate_field_name...There must be a field to customized a validation
    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError(
                detail="No cart with the given ID was found."
            )
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError(detail="The cart is empty")

        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            (customer, _) = Customer.objects.get_or_create(
                user_id=self.context["user_id"]
            )

            order = Order.objects.create(customer=customer)

            # Get cart items of the created cart_id
            cart_items = CartItem.objects.select_related("product").filter(
                cart_id=self.validated_data["cart_id"]
            )
            # Convert the cart items to order items using list comphren.
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    unit_price=item.product.unit_price,
                    quantity=item.quantity,
                )
                for item in cart_items
            ]
            # Save the order items using bulk create to save the list of order items at once
            OrderItem.objects.bulk_create(order_items)

            # Delete the cart id after creating an order
            Cart.objects.filter(pk=self.validated_data["cart_id"]).delete()

            order_created.send_robust(sender=self.__class__, order=order)

            return order
