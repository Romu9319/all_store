from django.shortcuts import render, redirect

import requests

import difflib

# Create your views here.
""" Vista catalogo de productos """
def index(request):
    url_products = "https://fakestoreapi.com/products"
    response = requests.get(url_products)

    if response.status_code == 200:               
        product_count = {}
        data = response.json() 

        for products in data:
            category = products["category"]
            product_count[category] = product_count.get(category,0)+1
           
        context = {
            "data": data,
            "categories": product_count
        }
        return render(request, "index.html", context)
    
    else: 
        return render(request, "index.html", {'error_message': f"Error al obtener datos: {response.status_code}"})
    

""" Vista de filtrado por categorias """    
def filterByCategory(request, category_name): 
    url_category = "https://fakestoreapi.com/products/category/" + category_name
    response = requests.get(url_category)

    if response.status_code == 200:
        products = response.json()

        context = {
            "data": products,
        }
        return render(request, "index.html", context)
    
    else: 
        return render(request, "index.html", {'error_message': f"Error al obtener datos: {response.status_code}"})


""" Vista de filtrado por nombres """
def filterByName(request):    
    name_get = request.GET.get("name", "")
    url_products = "https://fakestoreapi.com/products"
    response = requests.get(url_products)

    if response.status_code == 200:
        products = response.json()    
        filter_products = []

        for product in products:
            name = product.get("title", "")
            similarity_ratio = difflib.SequenceMatcher(None, name_get.lower(), name.lower()).ratio()
            print(f"name_get: {name_get}, name: {name}, similarity_ratio: {similarity_ratio}")

            if similarity_ratio > 0.2:
                filter_products.append(product)
        
        context = {
            "data": filter_products,
        }
        return render(request, "index.html", context)
    
    else: 
        return render(request, "index.html", {'error_message': f"Error al obtener datos: {response.status_code}"})
    

""" Vista de detalles de productos """
def productDetails(request, product_id):
    url_product = "https://fakestoreapi.com/products/" + product_id    
    response = requests.get(url_product)

    if response.status_code == 200:
        product = response.json()
        context = {
            "product": product,
        }
        return render(request, "detail.html", context)
    
    else:
        return render(request, "detail.html", {'error_message': f"Error al obtener datos: {response.status_code}"})
    
""" Vistas para el carro de compras """

from .shoppingCart import Cart

def shoppingCart(request):
    
    context= {
        "hola": "hola"
    }

    return render(request, "shoppingCart.html", context )

def addToCart(request, product_id):

    if request.method == 'POST':
        cuantity = int(request.POST["cuantity"])
    else:
        cuantity = 1
        
    url_product = "https://fakestoreapi.com/products/" + product_id
    response = requests.get(url_product)

    if response.status_code == 200:

        product = response.json()
        productCart = Cart(request)
        productCart.add(product, cuantity)

        if request.method == 'GET':
            return redirect("/")
        
        return render(request, "shoppingCart.html")
    
    else:
        return render(request, "shoppingCart.html", {'error_message': f"Error al obtener datos: {response.status_code}"})

def deleteProduct(request, product_id):
    
    url_product = "https://fakestoreapi.com/products/" + product_id
    response = requests.get(url_product)

    if response.status_code == 200:

        product = response.json()
        
        productCart = Cart(request)
        productCart.delete(product)

        return render(request, "shoppingCart.html")
    
    else:
        return render(request, "shoppingCart.html", {'error_message': f"Error al obtener datos: {response.status_code}"})

def clearCart(request):
    cartProduct = Cart(request)
    cartProduct.clear()

    return render(request, "shoppingCart.html")
