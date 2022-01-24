from django.contrib import admin

from .models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    A Tag Admin class for the instance of a tag model.

    Overridden options:
        search_fields: searchbox for product instances by label
    """
    search_fields = ['label']
