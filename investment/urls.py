from django.urls import path
from . import views

urlpatterns = [
    path('', views.investment, name='investment'),             
    path('new_investment/', views.add_investment, name="add_investment"),  
    path('edit/<int:id>/', views.edit_investment, name="edit_investment"),   
    path('delete/<int:id>/', views.delete_investment, name="delete_investment"), 
]