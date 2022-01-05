from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class LikedItem(models.Model):
    # what user likes what obj
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    # what object to like (e.g product, article, video)
    # TYPE (e.g Product, Article, Video)
    # ID (a particular row of interest)
    # content_obj (reading that obj)
    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()