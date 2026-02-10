from .models import Cart, CartItem
from .views import _cart_id

def counter(request):
    cart_count = 0

    # Skip admin
    if request.path.startswith('/admin') or request.path.startswith('/secureloginsite'):
        return {}

    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
        else:
            cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
            if cart:
                cart_items = CartItem.objects.filter(cart=cart)
            else:
                cart_items = []

        for item in cart_items:
            cart_count += item.quantity

    except Exception:
        cart_count = 0

    return {'cart_count': cart_count}
