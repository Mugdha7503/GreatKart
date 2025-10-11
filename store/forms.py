from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'product_name', 'desc', 'price', 'images', 'stock', 'is_available']