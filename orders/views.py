from django.shortcuts import render, redirect
from carts.models import CartItem 
from .forms import OrderForm
from .models import Order, Payment
import datetime,json

from django.http import HttpResponse

# Create your views here.
def payments(request):
    current_user = request.user
    body = json.loads(request.body)
    order = Order.objects.get(user=current_user, is_ordered=False, order_number=body['orderID'])

    payment = Payment(
        user = current_user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status']
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()
    
    return render(request,'orders/payments.html')


def place_order(request, total=0, quantity=0):
    current_user = request.user

    # If the cart count is less than or equal to 0, then redirect back to store
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    tax = 0
    grand_total = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        print('first if')
        if not form.is_valid():
            print(form.errors)

        if form.is_valid():
            # store all the billing information in order table
            print('2nd if')
            data = Order()
            print("storing")
            data.user           = current_user
            data.first_name     = form.cleaned_data['first_name']
            data.last_name      = form.cleaned_data['last_name']
            data.phone          = form.cleaned_data['phone']
            data.email          = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country        = form.cleaned_data['country']
            data.state          = form.cleaned_data['state']
            data.city           = form.cleaned_data['city']
            data.pincode        = form.cleaned_data['pincode']
            data.order_note     = form.cleaned_data['order_note']
            data.order_total    = grand_total
            data.tax            = tax
            data.ip             = request.META.get('REMOTE_ADDR')
            data.save()
            # print('stored1')
            # Genrate order number
            current_date = datetime.date.today().strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            # print('stored2')

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'tax':tax,
                'order' : order,
                'total': total,
                'grand_total': grand_total,
                'cart_items' : cart_items,
            }
            
            return render(request,'orders/payments.html', context)
        
    else:
        print("false")
        return redirect('checkout')