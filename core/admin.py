"""
An admin module that handles the linking of the store and tags app create independent principle between apps.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline

from store.admin import ProductAdmin, ProductImageInline
from store.models import Product
from tags.models import TaggedItem
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "email",
                    "first_name",
                    "last_name",
                ),
            },
        ),
    )


class TagInline(GenericTabularInline):
    """
    TaggedItem instance(s) to be used inline with the CustomProductAdmin interface

    Overridden options:
        autocomplete_fields: search and dropdown list for many2one OR many2many
        extra: number of pre-open orderitem form
        model: model to use
    """

    autocomplete_fields = ["tag"]
    extra = 0
    model = TaggedItem


class CustomProductAdmin(ProductAdmin):
    """
    A CustomProductAdmin class that extends the store/admin/ProductAdmin class by inheriting from it so as to decouple the dependence of store and tags app together.

    Args:
        inlines: TagInline
    """

    inlines = [TagInline, ProductImageInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
