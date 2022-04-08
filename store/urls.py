from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)

products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, 'product-reviews')

urlpatterns = router.urls + products_router.urls


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