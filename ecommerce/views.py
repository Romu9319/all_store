from django.shortcuts import render

# Create your views here.
"""Vista catalogo de productos"""

def index(request):
    return render(request,"index.html")