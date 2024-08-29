from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Product, User, Engagement, Feedback, Message, Profile, SupportInquiry, ProductEngagementSummary
import json

def home(request):
    return render(request, 'views/index.html')

def view(request):
    return render(request, 'views/view.html')

def products(request):
    all_products = Product.objects.all()
    context = {'products': all_products}
    return render(request, 'views/products.html', context)

def ecom(request):
    all_products = ProductEngagementSummary.objects.all()
    context = {'products': all_products}
    return render(request, 'views/ecom.html', context)

def users(request):
    all_users = User.objects.all()
    context = {'users': all_users}
    return render(request, 'views/users.html', context)

def engagements(request):
    all_engagements = Engagement.objects.all()
    context = {'engagements': all_engagements}
    return render(request, 'views/engagement.html', context)

def feedbacks(request):
    all_feedbacks = Feedback.objects.all()
    context = {'feedbacks': all_feedbacks}
    return render(request, 'views/feedback.html', context)

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
    return render(request, 'views/support.html', context)

@csrf_exempt
def record_engagement(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        engagement_type = data.get('type')

        try:
            # Assuming you're using Django's authentication system
            user = User.objects.get(pk=1)  # Replace with actual user retrieval logic, e.g., request.user
            product = Product.objects.get(pk=product_id)

            # Create a new engagement record
            engagement = Engagement.objects.create(
                product=product,
                user=user,
                type=engagement_type
            )
            return JsonResponse({'status': 'success', 'message': 'Engagement recorded.'})
        except (User.DoesNotExist, Product.DoesNotExist) as e:
            return JsonResponse({'status': 'fail', 'message': str(e)})
    else:
        return JsonResponse({'status': 'fail', 'message': 'Invalid request method.'})
    
    
    
@csrf_exempt
def update_product(request, product_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            product = Product.objects.get(pk=product_id)
            product.title = data.get('title', product.title)
            product.description = data.get('description', product.description)
            product.category = data.get('category', product.category)
            product.price = data.get('price', product.price)
            product.stock = data.get('stock', product.stock)
            product.location = data.get('location', product.location)
            product.save()
            return JsonResponse({'status': 'success', 'message': 'Product updated successfully.'})
        except Product.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Product not found.'})
    else:
        return JsonResponse({'status': 'fail', 'message': 'Invalid request method.'})
    
    
    
@csrf_exempt
def add_product(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            description = data.get('description')
            category = data.get('category')
            price = data.get('price')
            stock = data.get('stock')
            location = data.get('location')

            # Create a new Product object and save it
            product = Product(
                title=title,
                description=description,
                category=category,
                price=price,
                stock=stock,
                location=location
            )
            product.save()

            return JsonResponse({'status': 'success', 'message': 'Product added successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})