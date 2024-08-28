from django.shortcuts import render
from .models import Product, User, Engagement, Feedback, Message, Profile, SupportInquiry

def home(request):
    return render(request, 'views/index.html')

def products(request):
    all_products = Product.objects.all()
    context = {'products': all_products}
    return render(request, 'views/products.html', context)

def users(request):
    all_users = User.objects.all()
    context = {'users': all_users}
    return render(request, 'views/users.html', context)

def engagements(request):
    all_engagements = Engagement.objects.all()
    context = {'engagements': all_engagements}
    return render(request, 'views/engagements.html', context)

def feedbacks(request):
    all_feedbacks = Feedback.objects.all()
    context = {'feedbacks': all_feedbacks}
    return render(request, 'views/feedbacks.html', context)

def messages(request):
    all_messages = Message.objects.all()
    context = {'messages': all_messages}
    return render(request, 'views/messages.html', context)

def profiles(request):
    all_profiles = Profile.objects.all()
    context = {'profiles': all_profiles}
    return render(request, 'views/profiles.html', context)

def support_inquiries(request):
    all_inquiries = SupportInquiry.objects.all()
    context = {'inquiries': all_inquiries}
    return render(request, 'views/support_inquiries.html', context)
