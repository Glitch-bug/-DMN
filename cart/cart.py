from decimal import *
from store.models import Product
from django.core.exceptions import EmptyResultSet
class Cart():
    """
    A base Cart class, providing some default behaviour that
    can be inheried
    """
    def __init__(self, request):
        self.session = request.session
        print(self.session)
        cart = self.session.get('skey')

        if 'skey' not in request.session:
            cart = self.session['skey'] = {}
        self.cart = cart

    def add(self, product, qty):
        """
        Adding and updating the user cart session data
        """
        product_id = str(product['id'])

        if product_id in self.cart:
            self.cart[product_id]['qty'] = qty
            self.cart[product_id]['sb_total_price'] =  int(qty) * float(product['price'])
        else: 
            self.cart[product_id] = {
                'unit_price':str(product['price']),
                'qty':int(qty),
                'sb_total_price': int(qty) * float(product['price'])
            }
        self.save()
      
    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        print(self.cart.values())
        return sum(item['qty'] for item in self.cart.values())
    
    def get_abstotal_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

    def delete(self, product):
        """
        Delete item from session data
        """
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
        else:
            raise EmptyResultSet
        self.save()

    def save(self):
        self.session.modified = True