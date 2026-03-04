"""expenseTracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import include, path
import expenseTracker.views as views
from django.contrib.auth.views import LogoutView
from expenses import admin_views

urlpatterns = [
    # Main App Routes
    path('', views.home, name="home"),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('settings/', views.settings, name='settings'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    
    # Django Admin
    path('admin/', admin.site.urls),
    
    # App URLs (expenses અને investment)
    path('expenses/', include('expenses.urls')),
    path('investment/', include('investment.urls')),
    
    # ============ ADMIN PANEL ROUTES ============
    # Admin Login
    path('admin-login/', admin_views.admin_login, name='admin_login'),
    path('admin-logout/', admin_views.admin_logout, name='admin_logout'),
    
    # Admin Dashboard
    path('admin-dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    
    # Category Management
    path('admin-categories/', admin_views.admin_categories, name='admin_categories'),
    path('admin-categories/add/', admin_views.admin_add_category, name='admin_add_category'),
    path('admin-categories/<int:pk>/edit/', admin_views.admin_edit_category, name='admin_edit_category'),
    path('admin-categories/<int:pk>/delete/', admin_views.admin_delete_category, name='admin_delete_category'),
    
   
]