from django.contrib import admin
from django.urls import path
from jruapp import views  # Import views from your app

urlpatterns = [
    path('', views.home, name='home'),  # Reference the home view
    path('products', views.products, name='products'),  # Reference the home view
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),  # Reference the home view
]
