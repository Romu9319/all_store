
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static # permite agregar una ruta estática al urlpatterns 

urlpatterns = [ #los urlpatterns son las diferentes rutas de la aplicación 
    path("", include("ecommerce.urls")),
    path('admin/', admin.site.urls),    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
