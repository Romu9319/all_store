from django.shortcuts import render

import requests

# Create your views here.
"""Vista catalogo de productos"""

def index(request):
    url_products = "https://fakestoreapi.com/products"
    response = requests.get(url_products)

    if response.status_code == 200:
        categories = []
        data = response.json() 

        for products in data:
            if products["category"] not in categories:
                categories.append(products["category"] )

        context = {
            "data": data,
            "categories": categories
        }      

        return render(request, "index.html", context)
    
    else: 
        return render(request, "index.html", {'error_message': f"Error al obtener datos: {response.status_code}"})
    


