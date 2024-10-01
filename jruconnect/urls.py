from django.contrib import admin
from django.urls import path
from jruapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('home', views.home, name='home'),
    path('adminlog/', views.loginadmin, name='adminlog'),
    path('student/', views.loginstud, name='student'),
    path('products/', views.products, name='products'),
    path('ecom/', views.ecom, name='ecom'),
    path('record_engagement/', views.record_engagement, name='record_engagement'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),
    path('add_product/', views.add_product, name='add_product'),
    path('update-profile-image/', views.update_profile_image, name='update_profile_image'),
    # User-related URLs
    path('users/', views.users, name='users'),
    path('add-user/', views.add_user, name='add_user'),
    path('update-user/<int:user_id>/', views.update_user, name='update_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    
    # Engagement-related URLs
    path('engagements/', views.engagements, name='engagements'),
    path('add-engagement/', views.add_engagement, name='add_engagement'),
    path('update-engagement/<int:engagement_id>/', views.update_engagement, name='update_engagement'),
    path('delete-engagement/<int:engagement_id>/', views.delete_engagement, name='delete_engagement'),
    
    # Feedback-related URLs
    path('feedbacks/', views.feedbacks, name='feedbacks'),
    path('add-feedback/', views.add_feedback, name='add_feedback'),
    path('update-feedback/<int:feedback_id>/', views.update_feedback, name='update_feedback'),
    path('delete-feedback/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),
    
    # Message-related URLs
    path('messages/', views.messages, name='messages'),
    path('add-message/', views.add_message, name='add_message'),
    path('update-message/<int:message_id>/', views.update_message, name='update_message'),
    path('delete-message/<int:message_id>/', views.delete_message, name='delete_message'),
    
    # Profile-related URLs
    path('profiles/', views.profiles, name='profiles'),
    path('add-profile/', views.add_profile, name='add_profile'),
    path('update-profile/<int:profile_id>/', views.update_profile, name='update_profile'),
    path('delete-profile/<int:profile_id>/', views.delete_profile, name='delete_profile'),
    
    # Support Inquiry-related URLs
    path('support_inquiries/', views.support_inquiries, name='support_inquiries'),
    path('add-support-inquiry/', views.add_support_inquiry, name='add_support_inquiry'),
    path('update-support-inquiry/<int:inquiry_id>/', views.update_support_inquiry, name='update_support_inquiry'),
    path('delete-support-inquiry/<int:inquiry_id>/', views.delete_support_inquiry, name='delete_support_inquiry'),
       # Data fetching URLs
    path('get_engagements_by_type/', views.get_engagements_by_type, name='get_engagements_by_type'),
    path('get_support_inquiries_by_status/', views.get_support_inquiries_by_status, name='get_support_inquiries_by_status'),
    path('get_product_engagement_over_time/', views.get_product_engagement_over_time, name='get_product_engagement_over_time'),
    path('get_feedback_by_rating/', views.get_feedback_by_rating, name='get_feedback_by_rating'),
    path('chat_message/<int:user_id>/', views.chat_message, name='chat_message'),
    # Logout URL
    # Logout URL
    path('logout/', views.logout_view, name='logout'),
    
    path('admin/', admin.site.urls),
]
