""" 
This module provides the function to create a Product, Customer, Address, Collection... Data Model. 
"""
from django.db import models


class Promotion(models.Model):
    """
    A Promotion class for creating a Promotion obj.

    Fields:
        description (str): The field describe what the promotion is all about.
        discount (float): The field for the discount amount offered.
    """

    description = models.CharField(max_length=255)
    discount = models.FloatField()
    #! To do: add start and end date & time of promotion


class Collection(models.Model):
    """
    A Collection class for creating a Collection obj.

    Fields:
        title (str): The field for the title of the collection.
        featured_product (int): The field for connecting many collection to a product (use to advertize a collection).
    """

    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        to="Product", on_delete=models.SET_NULL, null=True, related_name="+"
    )


class Product(models.Model):
    """
    A Product class for creating a Product obj.

    Fields:
        title (str): The field for adding the title of a product.
        slug (str): The field for adding the slug (Search Engine Optimal)
        description (str): The field for adding the description of a product.
        price (int): The field for adding the price of a product.
        inventory (int): The field for adding the number of the product available.
        last_update (int): The field for adding the date and time at which a product is updated.
        collection (int): The field for connecting many products to a collection.
        promotions (int): The field for connecting many products to many collections.
    """

    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(to=Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(to=Promotion)


class Cart(models.Model):
    """
    A Cart class for creating a Cart obj.

    Field:
        created_at = The field for noting the day and time a cart obj is created.
    """

    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    """
    A CartItem class for creating a CartItem obj.

    Fields:
        cart (int): The field for connecting many cartitems to a cart.
        product (int): The field for connecting many cartitems to a product.
        quantity (int): The field for noting the number of items in a cart
    """

    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()


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
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE
    )
    
    class Meta:
        indexes = [
            models.Index(fields=['first_name', 'last_name'])
        ]


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
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING
    )
    customer = models.ForeignKey(to=Customer, on_delete=models.PROTECT)


class Address(models.Model):
    """
    An Address class for creating an address obj.

    Fields:
        street (str): The field for adding the street address.
        city (str): The field for adding the city address.
        customer (int): The field for connecting many addresses to a customer.
    """

    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.PositiveSmallIntegerField()
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE)


class OrderItem(models.Model):
    """
    An OrderItem class for creating an orderitem obj.

    Fields:
        order (int): The field for connecting many orderitems to an order.
        product (int): The field for connecting many orderitems to a product.
        quantity (int): The field for noting the quantity of orderitem.
        unit_price (float): The field for taking note of the price at which an orderitem instance occurred.
    """

    order = models.ForeignKey(to=Order, on_delete=models.PROTECT)
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
