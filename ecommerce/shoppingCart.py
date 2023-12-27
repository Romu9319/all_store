
class Cart:

    def __init__(self, request):
        self.request = request
        self.session = request.session
        
        cart = self.session.get("cart")

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart
    
    def add(self, product, cuantity):
        product_id = str(product["id"])
        
        self.cart[product_id] = {
            "product_id": product_id,
            "title": product["title"],
            "price": str(product["price"]),
            "category": product["category"],
            "description": product["description"],
            "image": product["image"],
            "subtotal": str(cuantity * product["price"])
        }

        self.save()

    def save(self):
        self.session["cart"] = self.cart
        self.session.modified = True