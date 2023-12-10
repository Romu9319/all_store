from django.contrib import admin

# Register your models here.
from .models import Category, Product
# Incluyo los modelos de mis tablas en el panel de administración 
admin.site.register(Category)
#admin.site.register(Product)

#los decoradores(@) permiten añadir funcionalidades especiales
@admin.register(Product)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("name","price","category", "singup_date") # list_display permite mostrar de forma personalizada los atributos de la calse Producto
    list_editable = ("price",)