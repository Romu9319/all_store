
class Cart:

    def __init__(self, request):
        self.request = request
        self.session = request.session
        
        cart = self.session.get("cart")
        totalAmount = self.session.get("totalAmount")

        if not cart:
            cart = self.session['cart'] = {}
            totalAmount = self.session['totalAmount'] = "0"

        self.cart = cart
        self.totalAmount = float(totalAmount)
    
    def add(self, product, cuantity):
        # verifica si el producto no se ha agregado anteriormente y de ser asi lo agregas 
        if str(product["id"]) not in self.cart.keys():
            
            product_id = str(product["id"])
            
            self.cart[product_id] = {
                "product_id": product_id,
                "title": product["title"],
                "price": str(product["price"]),
                "cuantity": cuantity,
                "category": product["category"],
                "description": product["description"],
                "image": product["image"],
                "subtotal": str(cuantity * product["price"])
            }
        else: # Actualizamos la cantidad y el subtotal del producto en caso de que se agrege nuevamente 
            for key,value in self.cart.items():              
                if key == str(product["id"]):
                    value["cuantity"] = str(int(value["cuantity"]) + cuantity)
                    value["subtotal"] = str(float(value["cuantity"]) * float(value["price"]))
                    break
        
        self.save()

    def delete(self, product):  
        product_id = str(product["id"])
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
                
    def clear(self):
        self.session["cart"] = {}
        self.session["totalAmount"] = "0"

    def save(self):
        totalAmount = 0

        for key, value in self.cart.items():
            totalAmount += float(value["subtotal"])

        self.session["cart"] = self.cart
        self.session["totalAmount"] = round(totalAmount, 2)
        self.session.modified = True