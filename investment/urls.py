from django.urls import path
from . import views

urlpatterns = [
    path('', views.investment, name='investment'),                 # READ
    path('new_investment/', views.add_investment, name="add_investment"),  # CREATE
    
    # ➕ ADD THESE
    path('edit/<int:id>/', views.edit_investment, name="edit_investment"),   # UPDATE
    path('delete/<int:id>/', views.delete_investment, name="delete_investment"), # DELETE
]