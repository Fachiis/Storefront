from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)

products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')  # product_pk
products_router.register('reviews', views.ReviewViewSet, 'product-reviews')
# product-reviews-list product-reviews-detail

carts_router = routers.NestedDefaultRouter(
    router, 'carts', lookup='cart')  # cart_pk
carts_router.register('items', views.CartItemViewSet, 'cart-items')
# cart-items-list cart-items-detail

urlpatterns = router.urls + products_router.urls + carts_router.urls


# urlpatterns = [
# If you have other complex patterns you want to use
#     path('', include(router.urls)),
#     path('', include(products_routers.urls)),
#     # path('products/', views.ProductList.as_view()),
#     # path("products/<int:pk>/", views.ProductDetail.as_view()),
#     # path('collections/', views.CollectionList.as_view()),
#     # path("collections/<int:pk>/", views.CollectionDetail.as_view(),
#     #      name="collection-detail"),
# ]
