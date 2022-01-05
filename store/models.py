""" 
This module provides the function to create Store Data Model which comprises of a Product, Customer, Address, Collection and Order object. 
"""
from django.db import models


class Promotion(models.Model):
    # To do: add start and end date & time of promotion
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(to="Product", on_delete=models.SET_NULL, null=True, related_name='+')


class Product(models.Model):
    """
    A Product class for creating a Product obj.

    Fields:
    title (str): The field column for adding the title of a product.
    description (str): The field column for adding the description of a product.
    price (int): The field column for adding the price of a product.
    inventory (int): The field column for adding the number of the product available.
    last_update (int): The field column for adding the date and time at which a product is updated.
    """

    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(to=Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(to=Promotion)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()


class Customer(models.Model):
    """
    A Customer class for creating a Customer obj.

    Fields:
    first_name (str): The field column for adding the first name of a customer.
    last_name (str): The field column for adding the last name of a customer.
    email (str): The field column for adding the email address of a customer (no duplicates).
    phone (str): The field column for adding the phone number of a customer.
    birthday (int): The field column for adding the birth day of a customer (optional).
    membership (str): The field column for adding the rank of a customer.
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


class Order(models.Model):
    """
    A Order class for creating an order obj.

    Fields:
    placed_at (int): The field column for adding the date and time at which an order is placed.
    payment_status (int): The field column for adding the status of the payment

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
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE)


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.PROTECT)
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
