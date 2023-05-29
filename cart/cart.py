from decimal import *
from store.models import Product

class Cart():
    """
    A base Cart class, providing some default behaviour that
    can be inheried
    """
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('skey')

        if 'skey' not in request.session:
            cart = self.session['skey'] = {}
        self.cart = cart

    def add(self, product, qty):
        """
        Adding and updating the user cart session data
        """
        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id]['qty'] = qty
        else: 
            self.cart[product_id] = {
                'price':str(product.price),
                'qty':int(qty)
            }
        self.save()
    
    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        return sum(item['qty'] for item in self.cart.values())

    def delete(self, product):
        """
        Delete item from session data
        """
        product_id = str(product)
        if product_id in self.basket:
            del self.basket[product_id]
        self.save()
