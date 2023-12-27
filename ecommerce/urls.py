from django.urls import path

from . import views

app_name = "ecommerce" # indica en que ubicación esta una vista que se quiera referencial para enlazar con una URL

urlpatterns = [ #los urlpatterns son las diferentes rutas de la aplicación 
    path('', views.index, name="index"),
    path('filterByCategory/<str:category_name>', views.filterByCategory, name="filterByCategory"),
    path('filterByName', views.filterByName, name='filterByName'),
    path('productDetails/<str:product_id>', views.productDetails, name="productDetails" ),
    path('cart', views.shoppingCart, name="shoppingCar"),
    path('addToCart/<str:product_id>', views.addToCart, name="addToCart")
] 