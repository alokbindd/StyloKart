from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse
from store.models import Product


def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('created_at')

    # Hero content: can later be loaded from a model (e.g. HeroSection) for Django admin
    hero_image = static('images/banners/banner1.webp')
    # Optional: prefer webp when available for production
    # hero_image = static('images/banners/banner1.webp')
    context = {
        'products': products,
        'hero_image': hero_image,
        'hero_title': 'Welcome to StyloKart',
        'hero_subtitle': 'Discover style that fits you. Shop the latest trends.',
        'hero_button_text': 'Shop Now',
        'hero_button_link': reverse('store'),
    }

    return render(request, 'home.html', context)