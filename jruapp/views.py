from django.http import JsonResponse, HttpResponseForbidden
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
def delete_product(request, product_id):
    if request.method == 'DELETE':
        try:
            product = Product.objects.get(pk=product_id)
            product.delete()
            return JsonResponse({'status': 'success'})
        except Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found'})
    else:
        return HttpResponseForbidden()

    
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

def users(request):
    all_users = User.objects.all()
    context = {'users': all_users}
    return render(request, 'views/users.html', context)

def engagements(request):
    all_engagements = Engagement.objects.all()
    users = User.objects.all()
    products = Product.objects.all()
    context = {
        'engagements': all_engagements,
        'users': users,
        'products': products,
    }
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

# Create Views
@csrf_exempt
def add_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            user = User(username=username, email=email)
            user.save()
            return JsonResponse({'status': 'success', 'message': 'User added successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def add_engagement(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product')
            user_id = data.get('user')
            engagement_type = data.get('type')
            user = User.objects.get(pk=user_id)
            product = Product.objects.get(pk=product_id)
            engagement = Engagement(product=product, user=user, type=engagement_type)
            engagement.save()
            return JsonResponse({'status': 'success', 'message': 'Engagement added successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def add_feedback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            content = data.get('content')
            rating = data.get('rating')
            user = User.objects.get(pk=user_id)
            feedback = Feedback(user=user, content=content, rating=rating)
            feedback.save()
            return JsonResponse({'status': 'success', 'message': 'Feedback added successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def add_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            content = data.get('content')
            user = User.objects.get(pk=user_id)
            message = Message(user=user, content=content)
            message.save()
            return JsonResponse({'status': 'success', 'message': 'Message added successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def add_profile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            bio = data.get('bio')
            user = User.objects.get(pk=user_id)
            profile = Profile(user=user, bio=bio)
            profile.save()
            return JsonResponse({'status': 'success', 'message': 'Profile added successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def add_support_inquiry(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            inquiry = data.get('inquiry')
            user = User.objects.get(pk=user_id)
            support_inquiry = SupportInquiry(user=user, inquiry=inquiry)
            support_inquiry.save()
            return JsonResponse({'status': 'success', 'message': 'Support Inquiry added successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

# Update Views
@csrf_exempt
def update_user(request, user_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User.objects.get(pk=user_id)
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.save()
            return JsonResponse({'status': 'success', 'message': 'User updated successfully!'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'User not found.'})
    else:
        return JsonResponse({'status': 'fail', 'message': 'Invalid request method.'})
@csrf_exempt
def update_engagement(request, engagement_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            engagement = Engagement.objects.get(pk=engagement_id)
            
            # Update the fields
            engagement.user_id = data.get('user')
            engagement.product_id = data.get('product')
            engagement.type = data.get('type')
            
            engagement.save()
            return JsonResponse({'status': 'success', 'message': 'Engagement updated successfully!'})
        except Engagement.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Engagement not found.'})
    else:
        return JsonResponse({'status': 'fail', 'message': 'Invalid request method.'})
    
@csrf_exempt
def update_feedback(request, feedback_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            feedback = Feedback.objects.get(pk=feedback_id)
            feedback.content = data.get('content', feedback.content)
            feedback.rating = data.get('rating', feedback.rating)
            feedback.save()
            return JsonResponse({'status': 'success', 'message': 'Feedback updated successfully!'})
        except Feedback.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Feedback not found.'})
    else:
        return JsonResponse({'status': 'fail', 'message': 'Invalid request method.'})

@csrf_exempt
def update_message(request, message_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = Message.objects.get(pk=message_id)
            message.content = data.get('content', message.content)
            message.save()
            return JsonResponse({'status': 'success', 'message': 'Message updated successfully!'})
        except Message.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Message not found.'})
    else:
        return JsonResponse({'status': 'fail', 'message': 'Invalid request method.'})

@csrf_exempt
def update_profile(request, profile_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            profile = Profile.objects.get(pk=profile_id)
            profile.bio = data.get('bio', profile.bio)
            profile.save()
            return JsonResponse({'status': 'success', 'message': 'Profile updated successfully!'})
        except Profile.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Profile not found.'})
    else:
        return JsonResponse({'status': 'fail', 'message': 'Invalid request method.'})

@csrf_exempt
def update_support_inquiry(request, inquiry_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            support_inquiry = SupportInquiry.objects.get(pk=inquiry_id)
            support_inquiry.inquiry = data.get('inquiry', support_inquiry.inquiry)
            support_inquiry.save()
            return JsonResponse({'status': 'success', 'message': 'Support Inquiry updated successfully!'})
        except SupportInquiry.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Support Inquiry not found.'})
    else:
        return JsonResponse({'status': 'fail', 'message': 'Invalid request method.'})

# Delete Views
@csrf_exempt
def delete_user(request, user_id):
    if request.method == 'DELETE':
        try:
            user = User.objects.get(pk=user_id)
            user.delete()
            return JsonResponse({'status': 'success'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'})
    else:
        return HttpResponseForbidden()

@csrf_exempt
def delete_engagement(request, engagement_id):
    if request.method == 'DELETE':
        try:
            engagement = Engagement.objects.get(pk=engagement_id)
            engagement.delete()
            return JsonResponse({'status': 'success'})
        except Engagement.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Engagement not found'})
    else:
        return HttpResponseForbidden()

@csrf_exempt
def delete_feedback(request, feedback_id):
    if request.method == 'DELETE':
        try:
            feedback = Feedback.objects.get(pk=feedback_id)
            feedback.delete()
            return JsonResponse({'status': 'success'})
        except Feedback.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Feedback not found'})
    else:
        return HttpResponseForbidden()

@csrf_exempt
def delete_message(request, message_id):
    if request.method == 'DELETE':
        try:
            message = Message.objects.get(pk=message_id)
            message.delete()
            return JsonResponse({'status': 'success'})
        except Message.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Message not found'})
    else:
        return HttpResponseForbidden()

@csrf_exempt
def delete_profile(request, profile_id):
    if request.method == 'DELETE':
        try:
            profile = Profile.objects.get(pk=profile_id)
            profile.delete()
            return JsonResponse({'status': 'success'})
        except Profile.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Profile not found'})
    else:
        return HttpResponseForbidden()

@csrf_exempt
def delete_support_inquiry(request, inquiry_id):
    if request.method == 'DELETE':
        try:
            support_inquiry = SupportInquiry.objects.get(pk=inquiry_id)
            support_inquiry.delete()
            return JsonResponse({'status': 'success'})
        except SupportInquiry.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Support Inquiry not found'})
    else:
        return HttpResponseForbidden()

# Register Views in urls.py
