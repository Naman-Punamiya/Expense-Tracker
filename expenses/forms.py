from django import forms
from django.contrib.auth.models import User
from .models import Category, Expense, AdminUser

class AdminLoginForm(forms.Form):
    """Admin Login Form"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class CategoryForm(forms.ModelForm):
    """Category Add/Edit Form"""
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Category Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description',
                'rows': 3
            })
        }


class ExpenseForm(forms.ModelForm):
    """Expense Add/Edit Form"""
    class Meta:
        model = Expense
        fields = ['account', 'expenseName', 'category', 'date', 'amount', 'currency', 'description']
        widgets = {
            'account': forms.Select(attrs={'class': 'form-control'}),
            'expenseName': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Expense Name'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Amount',
                'step': '0.01'
            }),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description',
                'rows': 3
            })
        }