from django.urls import path
from . import views

urlpatterns = [

    path('', views.food_search, name='food_search'),
 #path('food/', views.nutrients_view, name='nutrients'),

]
