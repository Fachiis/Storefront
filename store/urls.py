from rest_framework_nested import routers

from . import views

# lookup -> will point to a single obj using (<lookup_name>_pk)
# basename -> generates name of views: <basename>-list view and <basename>-detail
# view of our viewset when we have overide the get_queryset method
router = routers.DefaultRouter()
router.register("products", views.ProductViewSet, basename="products") # basename is optional here. The routes generated will be products-list and products-detail: list view and detail view of our viewset:: /products/ and /products/<pk>/
router.register("collections", views.CollectionViewSet) #  /collections/ and /collections/<pk>/
router.register("carts", views.CartViewSet)
router.register("customer", views.CustomerViewSet)
router.register("orders", views.OrderViewSet, basename="orders")

products_router = routers.NestedDefaultRouter(router, "products", lookup="product") # lookup -> will point to a single obj using (<lookup_name>_pk)
products_router.register("reviews", views.ReviewViewSet, basename="product-reviews") # basename is optional here. The routes generated will be product-reviews-list and product-reviews-detail: list view and detail view of our viewset:: /products/<product_pk>/reviews/ and /products/<product_pk>/reviews/<pk>/
products_router.register("images", views.ProductImageViewSet, basename="product-images") # /products/<product_pk>/images/ and /products/<product_pk>/images/<pk>/

carts_router = routers.NestedDefaultRouter(router, "carts", lookup="cart") # lookup -> will point to a single obj using (<lookup_name>_pk)
carts_router.register("items", views.CartItemViewSet, basename="cart-items") # basename is optional here. The routes generated will be cart-items-list and cart-items-detail: list view and detail view of our viewset:: /carts/<cart_pk>/items/ and /carts/<cart_pk>/items/<pk>/

urlpatterns = router.urls + products_router.urls + carts_router.urls
