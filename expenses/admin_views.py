from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Category, Expense, AdminUser, Account
from .forms import AdminLoginForm, CategoryForm

# ============ ADMIN LOGIN ============
def admin_login(request):
    """Admin Login Page"""
    if request.user.is_authenticated:
        try:
            admin_user = AdminUser.objects.get(user=request.user, is_admin=True)
            return redirect('admin_dashboard')
        except AdminUser.DoesNotExist:
            pass
    
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                try:
                    admin_user = AdminUser.objects.get(user=user, is_admin=True)
                    login(request, user)
                    messages.success(request, f'Welcome {username}!')
                    return redirect('admin_dashboard')
                except AdminUser.DoesNotExist:
                    messages.error(request, 'You are not authorized as Admin!')
            else:
                messages.error(request, 'Invalid username or password!')
    else:
        form = AdminLoginForm()
    
    return render(request, 'admin_login.html', {'form': form})


def admin_logout(request):
    """Admin Logout"""
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('admin_login')


# ============ ADMIN DECORATOR ============
def admin_required(view_func):
    """Check if user is Admin"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('admin_login')
        try:
            AdminUser.objects.get(user=request.user, is_admin=True)
            return view_func(request, *args, **kwargs)
        except AdminUser.DoesNotExist:
            messages.error(request, 'Admin access required!')
            return redirect('admin_login')
    return wrapper


# ============ ADMIN DASHBOARD ============
@admin_required
def admin_dashboard(request):
    """Admin Dashboard - Main Page"""
    categories = Category.objects.all()
    accounts = Account.objects.all()
    
    context = {
        'categories': categories,
        'total_categories': categories.count(),
        'total_accounts': accounts.count(),
    }
    
    return render(request, 'admin_dashboard.html', context)


# ============ CATEGORY MANAGEMENT ============
@admin_required
def admin_categories(request):
    """List all Categories"""
    categories = Category.objects.all()
    return render(request, 'admin_categories.html', {'categories': categories})


@admin_required
def admin_add_category(request):
    """Add New Category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('admin_categories')
    else:
        form = CategoryForm()
    
    return render(request, 'admin_category_form.html', {'form': form, 'title': 'Add Category'})


@admin_required
def admin_edit_category(request, pk):
    """Edit Category"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('admin_categories')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'admin_category_form.html', {'form': form, 'title': 'Edit Category'})


@admin_required
def admin_delete_category(request, pk):
    """Delete Category"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('admin_categories')
    
    return render(request, 'admin_confirm_delete.html', {'object': category, 'type': 'Category'})