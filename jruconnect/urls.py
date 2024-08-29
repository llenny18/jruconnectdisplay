from django.contrib import admin
from django.urls import path
from jruapp import views  # Import views from your app

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('view/', views.view, name='view'),
    path('ecom/', views.ecom, name='ecom'),
    path('users/', views.users, name='users'),
    path('engagements/', views.engagements, name='engagements'),
    path('feedbacks/', views.feedbacks, name='feedbacks'),
    path('messages/', views.messages, name='messages'),
    path('profiles/', views.profiles, name='profiles'),
    path('support_inquiries/', views.support_inquiries, name='support_inquiries'),
    path('admin/', admin.site.urls),
]