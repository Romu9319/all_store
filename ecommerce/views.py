from django.shortcuts import render

import requests

# Create your views here.
"""Vista catalogo de productos"""

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
    
def filterByCategory(request, category_name):
    url = "https://fakestoreapi.com/products/category/" + category_name
    response = requests.get(url)
    print("CONTENIDO DE LA",url)

    if response.status_code == 200:

        products = response.json()

        context = {
            "categories": products,
        }
        print(products)
        return render(request, "index.html", context)
    
    else: 
        return render(request, "index.html", {'error_message': f"Error al obtener datos: {response.status_code}"})
