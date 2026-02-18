from django.urls import path
from . import views

urlpatterns = [
    path('',views.investment,name='investment'),
    path('new_investment/',views.add_investment,name="add_investment")
]