from django.urls import path
from . import views

urlpatterns = [
    path('',views.investment,name='investments'),
    path('new_investment/',views.add_investment,name="add_investment")
]