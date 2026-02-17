from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse
from store.models import Product, Banner


def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('created_at')
    store_url = reverse('store')
    banner_qs = Banner.objects.filter(is_active=True).order_by('display_order')
    banners = []

    for b in banner_qs:
        try:
            image_url = b.image.url
        except Exception:
            image_url = static('images/banners/hero.webp')

        banners.append({
            'title': b.title,
            'subtitle': b.subtitle,
            'image_url': image_url,
            'button_text': b.button_text or 'Shop Now',
            'button_link': b.button_link or store_url,
        })

    if not banners:
        banners = [{
            'title': 'Welcome to StyloKart',
            'subtitle': 'Discover style that fits you. Shop the latest trends.',
            'image_url': static('images/banners/hero.webp'),
            'button_text': 'Shop Now',
            'button_link': store_url,
        }]
    
    context = {
        'products': products,
        'banners': banners
    }

    return render(request, 'home.html', context)