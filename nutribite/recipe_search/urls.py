from django.urls import path
from . import views

urlpatterns = [

    path('', views.recipe_search, name='recipe_search'),
]