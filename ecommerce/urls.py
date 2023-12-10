from django.urls import path

from . import views

app_name = "ecommerce" # indica en que ubicación esta una vista que se quiera referencial para enlazar con una URL

urlpatterns = [ #los urlpatterns son las diferentes rutas de la aplicación 
    path('', views.index, name="index"),
] 