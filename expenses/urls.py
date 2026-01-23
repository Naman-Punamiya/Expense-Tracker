from django.urls import path

from expenseTracker import views
from .views import add_expenses

urlpatterns = [
    path('/newExpenses',add_expenses,name='expenses'),
    path('expenses/', views.expenses,name="expenses"),
    path('investment/', views.investment,name="investment"),
    path('settings/', views.settings,name="settings"),
]
