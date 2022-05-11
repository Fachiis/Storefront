"""
A module that handles the admin section of the store by registering and customizing the data model.
"""
from typing import Any
from django.contrib import admin, messages
from django.db.models import Count
from django.urls import reverse
from django.http import HttpRequest
from django.utils.html import format_html
from django.utils.http import urlencode
from django.db.models.query import QuerySet

from . import models


class InventoryFilter(admin.SimpleListFilter):
    """
    A customize Inventory Filter that returns Low to admin when the inventory is less than 10

    Returns:
        QuerySet: The result of the queryset
    """

    condition = "<10"
    parameter_name = "inventory"
    title = "inventory"

    def lookups(self, request: Any, model_admin: Any):
        """
        The filter lookups in the admin interface

        Args:
            request (Any): Any
            model_admin (Any): Any

        Returns:
            list_of_tuples: ('Code', 'Human_readable')
        """
        return [
            (self.condition, "Low"),
        ]

    def queryset(self, request: Any, queryset: QuerySet):
        if self.value() == self.condition:
            return queryset.filter(inventory__lt=10)


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ["thumbnail"]

    def thumbnail(self, instance: models.ProductImage):
        if instance.image.name != "":
            return format_html(f"<img src='{instance.image.url}' class='thumbnail' />")
        return ""


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    """
    A Product Admin class for the instance of a product model.

    Overridden options:
        actions: add form action to the instances of the product
        prepopulated_fields: prefill some fields with another fields
        autocomplete_fields: search and dropdown list for many2one OR many2many
        search_fields: searchbox for product instances by
        list_display: display selected fields to the user
        list_editable: selected fields that should be editable
        list_per_page: product instances per page
        list_select_related: queries reduction by many2one fields
        list_filter: side bar filter options

    Functions:
        collection_title
        inventory_status
    """

    actions = ["clear_inventory"]
    autocomplete_fields = ["collection"]
    inlines = [ProductImageInline]
    list_display = ["title", "unit_price", "inventory_status", "collection_title"]
    list_editable = ["unit_price"]
    list_per_page = 10
    list_select_related = ["collection"]
    list_filter = ["collection", "last_update", InventoryFilter]
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ["title"]

    def collection_title(self, product):
        """
        A customize field option of Product data model that return the collection title

        Args:
            product ([type]): instance of product

        Returns:
            collection_title (str): returns the product collection title
        """
        return product.collection.title

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        """
        A method that returns Low  or Ok if the product inventory field is less than 10 or more

        Args:
            product ([type]): instance of product

        Returns:
            Low|OK (str): returns Low  or Ok
        """
        return "Low" if product.inventory < 10 else "Ok"

    @admin.action(description="Clear selected product inventory")
    def clear_inventory(self, request: HttpRequest, queryset: QuerySet):
        """
        A custom action method that clears selected product inventory

        Args:
            request (HttpRequest): instance of request obj
            queryset (QuerySet): Queryset
        """
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request=request,
            message=f"{updated_count} products were updated successfully",
            level=messages.SUCCESS,
        )

    class Media:
        css = {"all": ["store/styles.css"]}


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    A Customer Admin class for the instance of customer model.

    Overridden options:
        list_display: display selected fields to the user
        list_editable: selected fields that should be editable
        list_per_page: product instances per page
        search_fields: searchbox for product instances
    """

    autocomplete_fields = ["user"]
    list_display = ["first_name", "last_name", "membership", "customer_orders"]
    list_editable = ["membership"]
    list_select_related = ["user"]
    list_per_page = 10
    ordering = ["user__first_name", "user__last_name"]
    search_fields = ["first_name__istartswith", "last_name__istartswith"]

    @admin.display(ordering="customer_orders")
    def customer_orders(self, customer):
        """
        A method that create a link to customer's orders from the Customer Admin interface

        Args:
            customer ([type]): instance of customer

        Returns:
            link: clickable click to customer's orders
        """
        url = (
            reverse("admin:store_order_changelist")
            + "?"
            + urlencode({"customer__id": str(customer.id)})
        )
        return format_html('<a href="{}">{}</a>', url, customer.customer_orders)

    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(customer_orders=Count("order"))


class OrderItemInline(admin.TabularInline):
    """
    OrderItem instance(s) to be used inline with the OrderAdmin interface

    Overridden options:
        autocomplete_fields: search and dropdown list for many2one OR many2many
        extra: number of pre-open orderitem form
        model: model to use
    """

    autocomplete_fields = ["product"]
    extra = 0
    model = models.OrderItem


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    """
    An Order Admin class for the instance order model.

    Overridden options:
        list_display: display selected fields to the user
        list_per_page: product instances per page
    """

    autocomplete_fields = ["customer"]
    inlines = [OrderItemInline]
    list_display = ["id", "customer", "payment_status", "placed_at"]
    list_per_page = 10


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    """
    A Customer Admin class for the customer data model.

    Overridden options:
        list_display: display selected fields to the user
        search_fields: searchbox for collection instances
        autocomplete_fields: search and dropdown list for many2one OR many2many

    Functions:
        products_count
        get_queryset(overridden function)
    """

    autocomplete_fields = ["featured_product"]
    list_display = ["title", "products_count"]
    search_fields = ["title__istartswith"]

    @admin.display(ordering="products_count")
    def products_count(self, collection):
        """
        A method that create a link to products count from the Collection Admin interface

        Args:
            collection ([type]): instance of collection

        Returns:
            link: clickable click to products count
        """
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"collection__id": str(collection.id)})
        )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(products_count=Count("products"))
