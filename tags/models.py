from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Tag(models.Model):
    label = models.CharField(max_length=255)
    

class TaggedItem(models.Model):
    # what tag label on tag item
    tag = models.ForeignKey(to=Tag, on_delete=models.CASCADE)
    # what object to tag (e.g product, article, video)
    # TYPE (Product, Article, Video)
    # ID (a particular row of interest)
     # content_obj (reading that obj)
    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    
