""" 
This module provides the function to create a Tag and TaggedItem Data Model. 
"""
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class TaggedItemManager(models.Manager):
    """
    A TaggedItemManager for creating a clean method for calling a object type and the object id.
    """

    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)

        return TaggedItem.objects.select_related("tag").filter(
            content_type=content_type, object_id=obj_id
        )


class Tag(models.Model):
    """
    A Tag class for creating a tag obj.

    Fields:
        label (str): The field for adding the label of a tag.
    """

    label = models.CharField(max_length=255)


class TaggedItem(models.Model):
    """
    A TagItem class for creating a tagitem obj.

    Fields:
        tag (str): The field for connecting many tagitems to a tag.
        Generic Relation Creation...
    """

    objects = TaggedItemManager()
    tag = models.ForeignKey(to=Tag, on_delete=models.CASCADE)
    # what object to tag (e.g product, article, video)
    # TYPE (Product, Article, Video)
    # ID (a particular row of interest)
    # content_obj (reading that obj)
    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
