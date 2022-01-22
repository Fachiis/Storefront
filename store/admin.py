"""
A module that handles the admin section of the store by registering and customizing the data model.
"""
from django.contrib import admin
from django.db.models import Count
from django.http import HttpRequest

from . import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    """
    A Product Admin class for the product data model.
    
    Overridden options:
        list_display
        list_editable
        list_per_page
        list_select_related
        
    Functions:
        collection_title
        inventory_status
    """
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        return 'Low' if product.inventory < 10 else 'Ok'


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    A Customer Admin class for the customer data model.
    
    Overridden options:
        list_display
        list_editable
        list_per_page
    """
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 10


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    """
    An Order Admin class for the order data model.
    
    Overridden options:
        list_display
        list_per_page
    """
    list_display = ['id', 'customer', 'payment_status', 'placed_at']
    list_per_page = 10


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    """
    A Customer Admin class for the customer data model.
    
    Overridden options:
        list_display
        
    Functions:
        products_count
        get_queryset(overridden function)
    """
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        return collection.products_count

    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(products_count=Count('product'))
