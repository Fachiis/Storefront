from django.dispatch import receiver

from store.signals import order_created


@receiver(order_created)
def on_order_created(sender, **kwargs):
    # There are various kwargs that are passed to the signal handler::
    #  1 - instance: the actual instance being saved
    #  2 - created: a boolean indicating if the instance was created
    #  3 - raw: a boolean indicating if the instance was saved using raw SQL
    #  4 - using: the database alias being used
    #  5 - Others: any other keyword arguments when the signal is sent like the order instance
    print(kwargs["order"])
