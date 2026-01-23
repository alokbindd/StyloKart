from django.db import models
from category.models import category
from django.urls import reverse
# Create your models here.

class Product(models.Model):
    product_name    = models.CharField(max_length=200,unique=True)
    slug            = models.SlugField(max_length=100)
    description     = models.TextField(max_length=250)
    product_images  = models.ImageField(upload_to='photos/product')
    price           = models.IntegerField()
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(category, on_delete=models.CASCADE)
    created_at      = models.DateTimeField(auto_now_add=True)
    modified_at     = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', kwargs={'category_slug':self.category.slug,'product_slug':self.slug})

    def __str__(self):
        return self.product_name
