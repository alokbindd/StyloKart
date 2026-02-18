from django.test import TestCase
from django.urls import reverse
from store.models import Product
from category.models import category

class HomePageTest(TestCase):

    def test_homepage_loads_successfully(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_homepage_context_contains_products(self):
        Category = category.objects.create(
            category_name="Test Category",
            slug="test-category"
        )

        Product.objects.create(
            product_name="Test Product",
            slug="test-product",
            price=100,
            is_available=True,
            category=Category,
            stock=200
        )

        response = self.client.get(reverse('home'))

        self.assertTrue('products' in response.context)
        self.assertEqual(len(response.context['products']), 1)
