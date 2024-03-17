from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save

from ..models import Customer


# Signal handler
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_from_new_user(sender, **kwargs):
    # There are various kwargs that are passed to the signal handler::
    #  1 - instance: the actual instance being saved
    #  2 - created: a boolean indicating if the instance was created
    #  3 - raw: a boolean indicating if the instance was saved using raw SQL
    #  4 - using: the database alias being used
    #  5 - Others: any other keyword arguments passed to the save() method
    if kwargs["created"]:
        Customer.objects.create(user=kwargs["instance"])
