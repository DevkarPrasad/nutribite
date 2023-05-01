from django.urls import path
from . import views
from django.conf.urls import include

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('food/', include('food_search.urls'), name='food_search'),
    path('recipes/', include('recipe_search.urls'), name='recipe_search'),
]
