from django.shortcuts import render
from django.db.models import Q, F, Sum, Count, Max, Min, Avg, Value, Func
from django.db import transaction
from django.db.models.functions import Concat
from django.contrib.contenttypes.models import ContentType

from store.models import Collection, Customer, Order, OrderItem, Product
from tags.models import TaggedItem


#! Transaction in the whole view function.
# @transaction.atomic()
def index(request):
    """
    Django Play ground for queries evaluation

    Returns:
        [Queryset]
    """
    #! Reverse Relation in Django happens bewteen models by attaching _set to the reverse relation. E.g for a Customer to access Order, because order have a forward relation with customer, customer can access order with reverse relation by calling "model_set" i.e "order_set". Like wise; Order calling out OrderItem by "orderitem_set". Like wise; Cart calling out Cartitem by "cartitem_set"

    #! queryset are lazy, they are not evaluate until it is called upon, providing the ability to chain the queryset
    # query_set = Product.objects.all() # This query_set return are instances of the product object

    # Iterating over the queryset evaluate the queryset
    # for product in query_set:
    #     print(product)

    # when we pass list over a queryset, evaluation occur
    # products = list(query_set)

    # when we call an object, evaluation occur
    # product = Product.objects.get(pk=3)

    #! Retrieving objects
    # all(), get(), filter(), first(), exists()
    # query_set = Product.objects.all().filter(pk=3).first()
    # exists = Product.objects.all().filter(pk=3).exists()

    #! Filtering objects
    # Filter by fields optionally add looks_up like: gt, lt, range, exact, iexact, contains, startswith etc
    # query_set = Product.objects.filter(unit_price__gt=50)
    # query_set = Product.objects.filter(unit_price__range=(20, 30)).reverse()
    # query_set = Product.objects.filter(collection__id__gt=3)
    # query_set = Product.objects.filter(title__icontains='coffee')
    # query_set = Product.objects.filter(title__icontains='coffee')
    # query_set = Product.objects.filter(last_update__year=2021)
    # query_set = Product.objects.filter(description__isnull=True)

    #! Complex looksup using Q object with the bitwise operator(|)
    # Combine queries with the AND logical operator
    # query_set = Product.objects.filter(inventory__lt=10, unit_price__gt=20)
    # query_set = Product.objects.filter(
    #     inventory__lt=10).filter(unit_price__gt=20)

    # Combine queries with the OR logical operator
    # query_set = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__gt=10))
    # query_set = Product.objects.filter(Q(inventory__lt=10) | ~Q(unit_price__gt=10))

    #! Referecing fields using F object
    # query_set = Product.objects.filter(unit_price=F('collection__id'))
    # query_set = Product.objects.filter(unit_price=F('inventory'))

    #! Sorting
    # sorting using the order_by method and earliest to return the first obj
    # query_set = Product.objects.order_by('unit_price', '-title')[0]
    # query_set = Product.objects.earliest('unit_price', '-title')

    #! Limiting results
    # Use the python slicing syntax [:]
    # 0, 1, 2, 3, 5
    # query_set = Product.objects.all()[:5]
    # 5, 6, 7, 8, 9

    #! Selecting fields to query
    # Use the values method, the queryset return instances of the product obj in dictionary format
    # query_set = Product.objects.values('id', 'title', 'unit_price', 'collection__title')
    # Use the values_list method, the queryset return instances of the product obj in tuple of each value format
    # Use the distinct method to return duplicates from a query_set

    #! Deferring fields
    # only method, the queryset return instances of the product obj and does not filter into foreign key fields.
    # query_set = Product.objects.only('id', 'title')
    # defer method, return instances of the product obj except the specify
    # query_set = Product.objects.defer('id', 'title')

    #! Selecting related objects (select_related, prefetch_related)
    # selected_related (1) at the end call
    # query_set = Product.objects.select_related('collection')
    # prefetch_related (n) at the end call
    # query_set = Product.objects.prefetch_related('promotions')
    # combine all related objects
    # query_set = Product.objects.select_related('collection').prefetch_related('promotions')

    #! Aggregate objects
    # Sum, Min, Max, Avg, Count class to perform aggregation on objects
    # result = Product.objects.aggregate(count=Count('id'), min_price=Min('unit_price'))
    # result = Product.objects.filter(collection__id=3).aggregate(
    #     count=Count('id'), min_price=Min('unit_price'), average_price=Avg('unit_price'))

    #! Annotating objects
    # Annotating here means, adding new field(s) in instances of an obj during queries
    # query_set = Customer.objects.annotate(is_active=Value(True), is_new=F('id') + (3*2))

    #! Calling Database functions
    # An SQL function Call. e.g CONCAT strings when executing queries
    # query_set = Customer.objects.annotate(
    #     # CONCAT
    #     full_name=Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT'))
    # Same query but using django's db model functions
    # query_set = Customer.objects.annotate(
    #     full_name=Concat('first_name', Value(' '), 'last_name'),
    # )

    #! Grouping Data
    # Group the customers that have placed orders and the count of the orders
    # result = Customer.objects.annotate(
    #     orders_count=Count('order')
    # )

    #! Quering Generic Relationships
    # The big picture... content_type_id(table of interest id location in content_type app), object_type_id(object of interest in the content_type_id)
    # content_type = ContentType.objects.get_for_model(Product)

    # query_set = TaggedItem.objects \
    #     .select_related('tag') \
    #     .filter(
    #         content_type=content_type,
    #         object_id=1
    #     )

    # If a defined custom manager
    # query_set = TaggedItem.objects_manager.get_tags_for(Product, 1)

    #! Understanding queryset cache
    # query_set = Product.objects.all()
    # Django hit the data base at the first call of executing the query set.
    # list(query_set)
    # Django will not hit the database again for the execution below but read from the cache data above.
    # list(query_set)
    # query_set[0]

    #! In relational databases, we should always create the parent record first before creating the child record, else this will sprint an error i.e you should not create an orderitem without a order(parent), you should not create a cartitem without a cart(parent)

    #! Creating objects
    # collection = Collection()
    # collection.title = "Video Games"
    # collection.featured_product = Product(pk=1)
    # collection.save()

    # Collection.objects.create(title="Video Games", featured_product=Product(pk=1))

    #! Updating objects
    # collection = Collection.objects.get(pk=13)
    # collection.featured_product = None
    # collection.save()

    # For optimization(Avoid early optimization)
    # Collection.objects.filter(pk=13).update(featured_product=None)

    #! Deleting objects
    # Delete a single obj
    # collection = Collection.objects.get(pk=13)
    # collection.delete()

    # Delete multiple objects
    # Collection.objects.filter(pk__gt=5).delete()

    #! Transactions
    # It works like this. Before calling a view function, Django starts a transaction. If the response is produced without problems, Django commits the transaction. If the view produces an exception, Django rolls back the transaction.

    # You may perform subtransactions using savepoints in your view code, typically with the atomic() context manager. However, at the end of the view, either all or none of the changes will be committed.

    # (.... some other codes above that we do not want to wrap in the transaction)

    # Transaction in the view code
    # the transaction will fail as there is no product with pk=-11
    with transaction.atomic():
        order = Order()
        order.customer = Customer(pk=1)
        order.save()

        item = OrderItem()
        item.order = order
        item.product = Product(pk=-11)
        item.quantity = 4
        item.unit_price = 120
        item.save()

    return render(request, "home.html", {"name": "Fachiis"})
