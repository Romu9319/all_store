from django.urls import path

from . import views

app_name = "ecommerce" # indica en que ubicación esta una vista que se quiera referencial para enlazar con una URL

urlpatterns = [ #los urlpatterns son las diferentes rutas de la aplicación 
    path('', views.index, name="index"),
    path('filterByCategory/<str:category_name>', views.filterByCategory, name="filterByCategory"),
    path('filterByName', views.filterByName, name="filterByName"),
    path('productDetails/<str:product_id>', views.productDetails, name="productDetails" ),
    path('cart', views.shoppingCart, name="shoppingCar"),
    path('addToCart/<str:product_id>', views.addToCart, name="addToCart"),
    path('deleteProduct/<str:product_id>', views.deleteProduct, name="deleteProduct"),
    path('clearCart', views.clearCart, name="clearCart"),
    path('singupUser', views.singupUser, name="singupUser"),
    path('loginUser', views.loginUser, name="loginUser"),
    path('logoutUser', views.logoutUser, name="logoutUser"),
    path('userAccount', views.userAccount, name="userAccount"),
    path('updateClient', views.updateClient, name="updateClient"),
    path('registerOrder', views.registerOrder, name="registerOrder"),
    path('confirmOrder', views.confirmOrder, name="confirmOrder"),
    path('thanks', views.thanks, name="thanks")
]   