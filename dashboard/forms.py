from django import forms
from food.models import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control'}),

        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title", "description", "category", "price", "cost", "image"]
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control'}),
            "description": forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            "cost": forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            "price": forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            "category": forms.Select(attrs={'class': 'form-control'}),
            # data-preview: dashboard-ui.js shows the chosen picture in #image-preview
            "image": forms.FileInput(attrs={
                        'class': 'form-control',
                        'data-preview': '#image-preview',
                    }
            ),
    }

class UserForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["first_name", "last_name", "phone_number"]
        widgets = {
            "first_name": forms.TextInput(attrs={'class': 'form-control'}),
            "last_name": forms.TextInput(attrs={'class': 'form-control'}),
            "phone_number": forms.TextInput(attrs={'class': 'form-control'}),
        }
