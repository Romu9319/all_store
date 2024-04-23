from django.urls import reverse
from django.shortcuts import render, redirect
from .models import Category, Product, Client, Order, OrderDetail
from paypal.standard.forms import PayPalPaymentsForm 
from django.core.mail import send_mail

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
    return render(request, "shoppingCart.html" )


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


# VISTA PARA CLIENTES Y USUARIOS
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .forms import ClientForm


def singupUser(request):
    
    if request.method == 'POST':
        dataUser = request.POST["newUser"]
        dataPassword = request.POST["newPassword"]

        newUser = User.objects.create_user(username=dataUser, password=dataPassword)
        
        if newUser is not None:
            login(request, newUser)
            return redirect("/userAccount")
        
    return render(request, "singUp.html")


def loginUser(request):
    landingPage = request.GET.get("next", None)
    context = {
        "destination": landingPage
    }

    if request.method == 'POST':
        dataUser = request.POST["user"]
        dataPassword = request.POST["password"]
        dataDestination = request.POST["destination"]

        userAuth = authenticate(request, username=dataUser, password=dataPassword)
        if userAuth is not None:
            login(request, userAuth)

            if dataDestination != "None":
                return redirect(dataDestination)
            
            return redirect("/userAccount")
        else:
            context = {
                "authError": "Email or password incorrect"
            }

    return render(request, "login.html",context)


def logoutUser(request):

    logout(request)
    return render(request, "login.html")


def userAccount(request):

    try:
        editClient = Client.objects.get(user = request.user)

        dataClient = {
            "name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "address": editClient.address,
            "phone": editClient.phone,
            "gender": editClient.gender,
            "birthdate": editClient.birthdate,
        }
    
    except:
        dataClient = {
            "name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email
        }

    clientForm = ClientForm(dataClient)
    context = {
        "clientForm": clientForm
    }

    return render(request, "userAccount.html", context)


def updateClient(request):
    menssage = ""

    if request.method == "POST":
        clientForm = ClientForm(request.POST)        
        if clientForm.is_valid():
            dataClient = clientForm.cleaned_data # clened_data prepara los datos para ser guardados en la DB

            # registro el nuevo cliente
            newClient, created = Client.objects.get_or_create(user=request.user)           
            newClient.address = dataClient["address"]
            newClient.phone = dataClient["phone"]   
            newClient.birthdate = dataClient["birthdate"]
            newClient.gender = dataClient["gender"]
            newClient.save()

            # actualizo el usuario(auth_user)
            userUpdate = User.objects.get(pk=request.user.id)
            userUpdate.first_name = dataClient["name"]
            userUpdate.last_name = dataClient["last_name"]
            userUpdate.email = dataClient["email"]
            userUpdate.save()

            menssage = "User update"

    context = {
        "menssage":menssage,
        "clientForm": clientForm
    }

    return render(request, "userAccount.html", context)


"""Vistas para procesos de compra"""
@login_required(login_url='/loginUser')
def registerOrder(request):
    
    try:
        editClient = Client.objects.get(user = request.user)

        dataClient = {
            "name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "address": editClient.address,
            "phone": editClient.phone,
            "gender": editClient.gender,
            "birthdate": editClient.birthdate,
        }
    
    except:
        dataClient = {
            "name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email
        }

    clientForm = ClientForm(dataClient)
    context = {
        'clientForm':clientForm
    }

    return render(request, "order.html", context)


@login_required(login_url='/login')
def confirmOrder(request):
    context = {}
    if request.method == "POST":
        #actualizamos usuario
        userUpdate = User.objects.get(pk=request.user.id)
        userUpdate.first_name = request.POST['name']
        userUpdate.last_name = request.POST['last_name']
        userUpdate.save()
        #registramos o actualizamos
        try: 
            customerOrder = Client.objects.get(user=request.user)
            customerOrder.phone = request.POST['phone']
            customerOrder.address = request.POST['address']
            customerOrder.save()
            
        except:
            customerOrder = Client()
            customerOrder.user = userUpdate
            customerOrder.phone = request.POST['phone']
            customerOrder.address = request.POST['address']
            customerOrder.save()

        # registramos pedido
        orderNumber = ''
        totalAmount = float(request.session.get("totalAmount"))
        newOrder = Order()
        newOrder.client = customerOrder
        newOrder.save()

        # Registramos el detalle del pedido
        orderCart = request.session.get('cart')
        for key, value in orderCart.items(): 

            orderProduct = "https://fakestoreapi.com/products/" + value["product_id"]
            response = requests.get(orderProduct)

            if response.status_code == 200:
                productDetail = response.json()

            detail = OrderDetail()
            detail.order = newOrder
            detail.product = productDetail
            detail.cuantity = int(value['cuantity'])
            detail.subtotal = float(value['subtotal'])
            detail.save()
            

        # actualizar pedido
        orderNumber = 'ORD' + newOrder.registration_date.strftime('%Y') + str(newOrder.id)
        newOrder.order_number = orderNumber
        newOrder.total_amount = totalAmount
        newOrder.save()

        #creo variable de session para pedido
        request.session['orderId'] = newOrder.id
            
        paypal_dict = {
            "business": "sb-nntlf27846788@business.example.com",
            "amount": totalAmount,
            "item_name": "Order Code" + orderNumber,
            "invoice": orderNumber,
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri('/thanks'),
            "cancel_return": request.build_absolute_uri('/'),
            }

        orderForm = PayPalPaymentsForm(initial=paypal_dict)
        
        context = {
                "order": newOrder,
                "orderForm": orderForm
            }       
        
    return render(request, "purchase.html", context)


@login_required(login_url='/login')
def thanks(request):
    paypalId = request.GET.get("PayerID", None)
    context = {}

    if paypalId is not None:
        orderId = request.session.get('orderId')
        order = Order.objects.get(pk=orderId)
        order.status = "1"
        order.save()
        context = {
            "order": order
        }
        send_mail(
            "Confirmacion de pedido",
            "Numero de pedido" + order.order_number,
            "danielerm1510@gmail.com",
            [request.user.email],
            fail_silently=False,
        )

    else:
        return redirect('/')

    cart = Cart(request)
    cart.clear()

    return render(request, "thanks.html", context)
# CREAR PLANTILLA DE AGRADECIMIENTO