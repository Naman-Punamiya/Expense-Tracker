from django.urls import path
from . import views
from . import admin_views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    
    # USER EXPENSE PAGE
    path('', views.expenses, name='expenses'),

    # ADD EXPENSE PAGE
    path('add/', views.add_expenses, name='add_expenses'),

    # EDIT EXPENSE
    path('expense/<int:id>/edit/', views.edit_expense, name='edit_expense'),

    # DELETE EXPENSE
    path('expense/<int:id>/delete/', views.delete_expense, name='delete_expense'),

    # ADMIN ROUTES
    path('admin-login/', admin_views.admin_login, name='admin_login'),
    path('admin-logout/', admin_views.admin_logout, name='admin_logout'),
    path('admin-dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('add-member/', views.add_member, name='add_member'),

    path('admin-categories/', admin_views.admin_categories, name='admin_categories'),
    path('admin-categories/add/', admin_views.admin_add_category, name='admin_add_category'),
    path('admin-categories/<int:pk>/edit/', admin_views.admin_edit_category, name='admin_edit_category'),
    path('admin-categories/<int:pk>/delete/', admin_views.admin_delete_category, name='admin_delete_category'),
]