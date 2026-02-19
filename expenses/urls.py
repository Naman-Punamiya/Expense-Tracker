from django.urls import path
from . import views

urlpatterns = [
    path('',views.expenses,name='expenses'),
    path('new_expense/', views.add_expenses,name="add_expenses"),
<<<<<<< HEAD
=======
    path('expense/<int:id>/edit/', views.edit_expense, name='edit_expense'),
    path('expense/<int:id>/delete/', views.delete_expense, name='delete_expense'),
>>>>>>> origin/naman
]
