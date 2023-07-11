"""
    The views for the playground app.
    """
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from store.models import Product


def all_orm(request):
    """
    All available ORM methods.

    Args:
        request (_type_): the request object
    Returns:
        _type_: _description_ 
    """

    # ** Retrieving objects **
    query_set = Product.objects.all()
    # ** When we use pk, django automatically transforms the pk to id, or code or uuid used in the model of interest. (Product)
    product = Product.objects.filter(pk=1).first()

    # ** Filtering Objs
    query_set2 = Product.objects.filter(unit_price__gt=20)
    query_set3 = Product.objects.filter(unit_price__range=(20, 30))


    return HttpResponse("Hello, world. You're at the playground view.")
