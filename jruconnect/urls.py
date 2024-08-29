from django.contrib import admin
from django.urls import path
from jruapp import views  # Import views from your app

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('record_engagement/', views.record_engagement, name='record_engagement'),
     path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),
    path('add_product/', views.add_product, name='add_product'),
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