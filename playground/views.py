from django.db.models import query
from django.http.response import HttpResponse
from django.shortcuts import render
from django.db.models import Q

from store.models import Product


def index(request):
    queryset = Product.objects.filter(Q(inventory__gt=10) | Q(unit_price__lt=20))
    
    return render(request, "home.html", {"name": "Fachiis", "products": list(queryset)})
