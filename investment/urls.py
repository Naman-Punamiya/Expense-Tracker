from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
 path('login/', auth_views.LoginView.as_view(template_name='project_login.html'), name='login'),

    path('', views.investment, name='investment'),             
    path('new_investment/', views.add_investment, name="add_investment"),  
    path('edit/<int:id>/', views.edit_investment, name="edit_investment"),   
    path('delete/<int:id>/', views.delete_investment, name="delete_investment"), 
     path('investment/', views.investment, name='investment'),
     
    

]