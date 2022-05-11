""" 
This module provides the function to create a Product, Customer, Address, Collection... Data Model. 
"""
from uuid import uuid4
from django.db import models
from django.conf import settings
from django.contrib import admin
from django.core.validators import MinValueValidator, FileExtensionValidator

from store.validators import validate_file_size


class Promotion(models.Model):
    """
    A Promotion class for creating a Promotion obj.

    Fields:
        description (str): The field describe what the promotion is all about.
        discount (float): The field for the discount amount offered.
    """

    description = models.CharField(max_length=255)
    discount = models.FloatField()
    # TODO: add start and end date & time of promotion


class Collection(models.Model):
    """
    A Collection class for creating a Collection obj.

    Fields:
        title (str): The field for the title of the collection.
        featured_product (int): The field for connecting many collection to a product.
    """

    featured_product = models.ForeignKey(
        to="Product", on_delete=models.SET_NULL, null=True, related_name="+"
    )
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]


class Product(models.Model):
    """
    A Product class for creating a Product obj.

    Fields:
        title (str): The field for adding the title of a product.
        slug (str): The field for adding the slug (Search Engine Optimal)
        description (str): The field for adding the description of a product (optional).
        price (int): The field for adding the price of a product.
        inventory (int): The field for adding the number of the product available.
        last_update (int): The field for adding the date and time at which a product is updated.
        collection (int): The field for connecting many products to a collection.
        promotions (int): The field for connecting many products to many collections.
    """

    collection = models.ForeignKey(
        to=Collection, on_delete=models.PROTECT, related_name="products"
    )
    description = models.TextField(null=True, blank=True)
    inventory = models.IntegerField(validators=[MinValueValidator(1)])
    last_update = models.DateTimeField(auto_now=True)
    promotions = models.ManyToManyField(to=Promotion, blank=True)
    slug = models.SlugField()
    title = models.CharField(max_length=255)
    unit_price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_images"
    )
    image = models.ImageField(
        upload_to="store/images",
        validators=[validate_file_size],
    )
    # files = models.FileField(
    #     upload_to="store/files",
    #     validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    # )


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    """
    A Cart class for creating a Cart obj.

    Field:
        created_at = The field for noting the day and time a cart obj is created.
    """

    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    """
    A CartItem class for creating a CartItem obj.

    Fields:
        cart (int): The field for connecting many cartitems to a cart.
        product (int): The field for connecting many cartitems to a product.
        quantity (int): The field for noting the number of items in a cart
    """

    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [["cart", "product"]]


class Customer(models.Model):
    """
    A Customer class for creating a Customer obj.

    Fields:
        first_name (str): The field for adding the first name of a customer.
        last_name (str): The field for adding the last name of a customer.
        email (str): The field for adding the email address of a customer (no duplicates).
        phone (str): The field for adding the phone number of a customer.
        birthday (int): The field for adding the birth day of a customer (optional).
        membership (str): The field for adding the rank of a customer.
    """

    MEMBERSHIP_BRONZE = "B"
    MEMBERSHIP_SILVER = "S"
    MEMBERSHIP_GOLD = "G"
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, "Bronze"),
        (MEMBERSHIP_SILVER, "Silver"),
        (MEMBERSHIP_GOLD, "Gold"),
    ]
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE
    )
    phone = models.CharField(max_length=255)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

    @admin.display(ordering="user__first_name")
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering="user__last_name")
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ["user__first_name", "user__last_name"]
        permissions = [("view_history", "Can view history")]


class Order(models.Model):
    """
    A Order class for creating an order obj.

    Fields:
        placed_at (int): The field for adding the date and time at which an order is placed.
        payment_status (int): The field for adding the status of the payment
    """

    PAYMENT_STATUS_PENDING = "P"
    PAYMENT_STATUS_COMPLETE = "C"
    PAYMENT_STATUS_FAILED = "F"
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, "Pending"),
        (PAYMENT_STATUS_COMPLETE, "Complete"),
        (PAYMENT_STATUS_FAILED, "Failed"),
    ]
    customer = models.ForeignKey(to=Customer, on_delete=models.PROTECT)
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING
    )

    class Meta:
        permissions = [("cancel_order", "Can cancel order")]


class Address(models.Model):
    """
    An Address class for creating an address obj.

    Fields:
        street (str): The field for adding the street address.
        city (str): The field for adding the city address.
        customer (int): The field for connecting many addresses to a customer.
    """

    city = models.CharField(max_length=255)
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    zip = models.PositiveSmallIntegerField()


class OrderItem(models.Model):
    """
    An OrderItem class for creating an orderitem obj.

    Fields:
        order (int): The field for connecting many orderitems to an order.
        product (int): The field for connecting many orderitems to a product.
        quantity (int): The field for noting the quantity of orderitem.
        unit_price (float): The field for taking note of the price at which an orderitem instance occurred.
    """

    order = models.ForeignKey(
        to=Order, on_delete=models.PROTECT, related_name="order_items"
    )
    product = models.ForeignKey(
        to=Product, on_delete=models.PROTECT, related_name="order_items"
    )
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
