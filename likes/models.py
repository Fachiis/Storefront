""" 
This module provides the function to create a LikedItem Data Model. 
"""
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class LikedItem(models.Model):
    """
    A LikedItem class for creating a likeditem obj.

    Fields:
        user (str): The field for connecting many likeditems to a user.
        Generic Relation Creation...
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    # what object to like (e.g product, article, video)
    # TYPE (e.g Product, Article, Video)
    # ID (a particular row of interest)
    # content_obj (reading that obj)
    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()