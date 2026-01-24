from django.urls import path
from . import views

urlpatterns = [
    path('',views.expenses,name='expenses'),
    path('new_expense/', views.add_expenses,name="add_expenses"),
]
