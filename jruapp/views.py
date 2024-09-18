from datetime import timezone
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout
from jruconnect import settings
from .models import Product, User, Engagement, Feedback, Message, Profile, SupportInquiry, ProductEngagementSummary, ViewEngagementsByType, ViewProductEngagementOverTime, ViewFeedbackByRating, ViewSupportInquiriesByStatus
import json
import os
from django.db.models import Q


def home(request):
    full_name = request.session.get('full_name', 'Guest')
    admin_id = request.session.get('admin_id', '0')
    role = request.session.get('role', '')
    # Fetch the admin user based on admin_id
    view_engagements_by_type = ViewEngagementsByType.objects.all()
    view_feedback_by_rating = ViewFeedbackByRating.objects.all()
    view_product_engagement_over_time = ViewProductEngagementOverTime.objects.all()
    view_support_inquiries_by_status = ViewSupportInquiriesByStatus.objects.all()
    admin_user = None
    if admin_id:
        try:
            admin_user = User.objects.get(user_id=admin_id)
        except User.DoesNotExist:
            admin_user = None  # Handle case where no admin user is found
    context = {
        'full_name': full_name, 'role':role,'admin_id' : admin_id, 'admin_user': admin_user , 'view_engagements_by_type': view_engagements_by_type, 'view_feedback_by_rating': view_feedback_by_rating,   'view_product_engagement_over_time': view_product_engagement_over_time,   'view_support_inquiries_by_status': view_support_inquiries_by_status
    }
    return render(request, 'views/index.html', context)


from django.http import JsonResponse
from .models import ViewEngagementsByType, ViewFeedbackByRating, ViewProductEngagementOverTime, ViewSupportInquiriesByStatus

def get_engagements_by_type(request):
    data = list(ViewEngagementsByType.objects.values('year', 'month', 'engagement_count', 'type'))
    return JsonResponse(data, safe=False)

def get_feedback_by_rating(request):
    data = list(ViewFeedbackByRating.objects.values('year', 'month', 'rating_count', 'rating'))
    return JsonResponse(data, safe=False)

def get_product_engagement_over_time(request):
    data = list(ViewProductEngagementOverTime.objects.values('year', 'month', 'engagement_count', 'product_id'))
    return JsonResponse(data, safe=False)

def get_support_inquiries_by_status(request):
    data = list(ViewSupportInquiriesByStatus.objects.values('year', 'month', 'status_count', 'status'))
    return JsonResponse(data, safe=False)



def view(request):
    return render(request, 'views/view.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Query the user by username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, 'views/login.html', {'error': 'Invalid credentials'})
        
        # Check password (assuming password_hash is a hashed password)
        if user.password_hash == password:  # Ideally, use a password hashing library
            request.session['admin_id'] = user.user_id  # Set session variable
            request.session['full_name'] = user.full_name  # Set session variable
            request.session['role'] = user.role  # Set session variable
            return redirect('home')
        else:
            return render(request, 'views/login.html', {'error': 'Invalid credentials'})
    return render(request, 'views/login.html')

def products(request):
    full_name = request.session.get('full_name', 'Guest')
    admin_id = request.session.get('admin_id', '0')
    # Fetch the admin user based on admin_id
    admin_user = None
    if admin_id:
        try:
            admin_user = User.objects.get(user_id=admin_id)
        except User.DoesNotExist:
            admin_user = None  # Handle case where no admin user is found
   
    all_products = Product.objects.all()
    context = {'products': all_products, 'full_name': full_name, 'admin_id' : admin_id, 'admin_user': admin_user }
    return render(request, 'views/products.html', context)



def ecom(request):
    full_name = request.session.get('full_name', 'Guest')
    admin_id = request.session.get('admin_id', '0')
    # Fetch the admin user based on admin_id
    admin_user = None
    if admin_id:
        try:
            admin_user = User.objects.get(user_id=admin_id)
        except User.DoesNotExist:
            admin_user = None  # Handle case where no admin user is found
    
    all_products = ProductEngagementSummary.objects.all()
    context = {'products': all_products, 'full_name': full_name, 'admin_id' : admin_id, 'admin_user': admin_user }
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
            # Get form data
            title = request.POST.get('title')
            description = request.POST.get('description')
            user_id = request.POST.get('user_id')
            category = request.POST.get('category')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            location = request.POST.get('location')

            # Handle image upload
            image = request.FILES.get('image')
            if image:
                # Use STATICFILES_DIRS or a specific directory inside the static folder
                image_folder = os.path.join(settings.BASE_DIR, 'staticfiles', 'images')
                if not os.path.exists(image_folder):
                    os.makedirs(image_folder)

                # Generate the file path using the product title
                image_name = f"{title.replace(' ', '_')}_{image.name}"
                image_path = os.path.join(image_folder, image_name)

                # Save the image to the static/images folder
                with open(image_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)

                # Build the image URL relative to the static folder
                image_url = f"/images/{image_name}"
            else:
                image_url = None

            # Create a new Product object and save it
            product = Product(
                title=title,
                user_id=user_id,
                description=description,
                category=category,
                price=price,
                stock=stock,
                location=location,
                image_url=image_url
            )
            product.save()

            return JsonResponse({'status': 'success', 'message': 'Product added successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def users(request):
    full_name = request.session.get('full_name', 'Guest')
    admin_id = request.session.get('admin_id', '0')
    # Fetch the admin user based on admin_id
    admin_user = None
    if admin_id:
        try:
            admin_user = User.objects.get(user_id=admin_id)
        except User.DoesNotExist:
            admin_user = None  # Handle case where no admin user is found
    all_users = User.objects.all()
    context = {'users': all_users, 'full_name': full_name, 'admin_id' : admin_id, 'admin_user': admin_user }
    return render(request, 'views/users.html', context)

def engagements(request):
    full_name = request.session.get('full_name', 'Guest')
    admin_id = request.session.get('admin_id', '0')
    # Fetch the admin user based on admin_id
    admin_user = None
    if admin_id:
        try:
            admin_user = User.objects.get(user_id=admin_id)
        except User.DoesNotExist:
            admin_user = None  # Handle case where no admin user is found
    all_engagements = Engagement.objects.all()
    users = User.objects.all()
    products = Product.objects.all()
    context = {
        'engagements': all_engagements,
        'users': users,
        'products': products,
        'full_name': full_name, 'admin_id' : admin_id, 'admin_user': admin_user 
    }
    return render(request, 'views/engagement.html', context)


def feedbacks(request):
    full_name = request.session.get('full_name', 'Guest')
    admin_id = request.session.get('admin_id', '0')
    # Fetch the admin user based on admin_id
    admin_user = None
    if admin_id:
        try:
            admin_user = User.objects.get(user_id=admin_id)
        except User.DoesNotExist:
            admin_user = None  # Handle case where no admin user is found
    all_feedbacks = Feedback.objects.all()
    users = User.objects.all()
    products = Product.objects.all()
    context = {'feedbacks': all_feedbacks, 
        'users': users,
        'products': products, 'full_name': full_name, 'admin_id' : admin_id, 'admin_user': admin_user }
    return render(request, 'views/feedback.html', context)

def messages(request):
    full_name = request.session.get('full_name', 'Guest')
    admin_id = request.session.get('admin_id', '0')
    # Fetch the admin user based on admin_id
    admin_user = None
    if admin_id:
        try:
            admin_user = User.objects.get(user_id=admin_id)
        except User.DoesNotExist:
            admin_user = None  # Handle case where no admin user is found
    all_messages = Message.objects.all()
    users = User.objects.all()
    context = {'messages': all_messages, 
        'users': users, 'full_name': full_name, 'admin_id' : admin_id, 'admin_user': admin_user }
    return render(request, 'views/messages.html', context)

def profiles(request):
    full_name = request.session.get('full_name', 'Guest')
    admin_id = request.session.get('admin_id', '0')
    # Fetch the admin user based on admin_id
    admin_user = None
    if admin_id:
        try:
            admin_user = User.objects.get(user_id=admin_id)
        except User.DoesNotExist:
            admin_user = None  # Handle case where no admin user is found
    all_profiles = Profile.objects.all()
    users = User.objects.all()
    context = {'profiles': all_profiles, 
        'users': users, 'full_name': full_name, 'admin_id' : admin_id, 'admin_user': admin_user }
    return render(request, 'views/profiles.html', context)

def support_inquiries(request):
    full_name = request.session.get('full_name', 'Guest')
    admin_id = request.session.get('admin_id', '0')
    # Fetch the admin user based on admin_id
    admin_user = None
    if admin_id:
        try:
            admin_user = User.objects.get(user_id=admin_id)
        except User.DoesNotExist:
            admin_user = None  # Handle case where no admin user is found
    all_inquiries = SupportInquiry.objects.all()
    users = User.objects.all()
    context = {'inquiries': all_inquiries, 
        'users': users, 'full_name': full_name, 'admin_id' : admin_id, 'admin_user': admin_user }
    return render(request, 'views/support.html', context)


def chat_message(request, user_id):
    full_name = request.session.get('full_name', 'Guest')
    admin_id = request.session.get('admin_id', '0')

    # Fetch the admin user based on admin_id
    admin_user = None
    if admin_id:
        try:
            admin_user = User.objects.get(user_id=admin_id)
        except User.DoesNotExist:
            admin_user = None  # Handle case where no admin user is found

    # Ensure admin_user exists before filtering messages
    if admin_user:
        # Filter messages where admin_id is either the sender or receiver and user_id is involved
        all_messages = Message.objects.filter(
            Q(sender_id=admin_id) | Q(receiver_id=admin_id),
            Q(sender_id=user_id) | Q(receiver_id=user_id)
        ).order_by('date_sent')  # Order by date ascending
    else:
        all_messages = Message.objects.none()  # Return an empty QuerySet if admin_user is not found

    # Separate users into senders and receivers
    senders = User.objects.filter(user_id=admin_id).distinct()
    receivers = User.objects.filter(user_id=user_id).distinct()
    sender_id = admin_id

    users = User.objects.all()

    context = {
        'sender_id': sender_id,
        'all_messages': all_messages,
        'senders': senders,
        'receivers': receivers,
        'users': users,
        'full_name': full_name,
        'admin_id': admin_id,
        'admin_user': admin_user
    }
    return render(request, 'views/chatmessage.html', context)



@csrf_exempt
def update_profile_image(request):
    if request.method == 'POST':
        try:
            user_id = request.POST.get('user_id')
            user = get_object_or_404(User, pk=user_id)

            # Handle image upload
            image = request.FILES.get('profile_image')
            if image:
                # Use STATICFILES_DIRS or a specific directory inside the static folder
                image_folder = os.path.join(settings.BASE_DIR, 'staticfiles', 'profile_images')
                if not os.path.exists(image_folder):
                    os.makedirs(image_folder)

                # Generate the file path using a unique name
                image_name = f"{user_id}_{image.name}"
                image_path = os.path.join(image_folder, image_name)

                # Save the image to the static/images folder
                with open(image_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)

                # Build the image URL relative to the static folder
                image_url = f"/profile_images/{image_name}"

                # Update the user's profile_image_url
                user.profile_url = image_url
                user.save()
                

                return JsonResponse({'status': 'success', 'message': 'Profile image updated successfully!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'No image file provided.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def logout_view(request):
    logout(request)  # This will clear the session data and log out the user
    return redirect('login')  # Redirect to the login page


@csrf_exempt
def add_user(request):
    if request.method == 'POST':
        try:
            # Handle file upload
            profile_image = request.FILES.get('profile_image')
            if profile_image:
                # Ensure correct handling of binary file
                image_path = os.path.join(settings.BASE_DIR, 'staticfiles','profile_images', profile_image.name)
                with open(image_path, 'wb+') as destination:
                    for chunk in profile_image.chunks():
                        destination.write(chunk)
                
                # Save the file path in the database
                profile_image_url = os.path.join('profile_images', profile_image.name)
            else:
                profile_image_url = None

            # Create user object and save
            user = User(
                username=request.POST.get('username'),
                full_name=request.POST.get('full_name'),
                email=request.POST.get('email'),
                password_hash=request.POST.get('password'),
                role=request.POST.get('role'),
                verified=request.POST.get('verified') == 'on',
                profile_url=profile_image_url
            )
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
            user_id = data.get('user')
            content = data.get('content')
            rating = data.get('rating')
            product_id = data.get('product')  # Get the product_id
            
            user = User.objects.get(pk=user_id)
            product = Product.objects.get(pk=product_id)  # Get the product

            feedback = Feedback(user=user, comment=content, rating=rating, product=product)  # Include product
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
            sender_id = data.get('sender_id')
            receiver_id = data.get('receiver_id')
            content = data.get('content')

            # Debugging output
            print("Received data:", data)

            sender = User.objects.get(pk=sender_id)
            receiver = User.objects.get(pk=receiver_id)

            message = Message(sender=sender, receiver=receiver, content=content)
            message.save()

            return JsonResponse({'status': 'success', 'message': 'Message added successfully!'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Sender or receiver not found'})
        except Exception as e:
            print("Error:", str(e))  # Debugging output
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


@csrf_exempt
def add_profile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            contact_number = data.get('contact')
            bio = data.get('bio')
            user = User.objects.get(pk=user_id)
            profile = Profile(user=user, bio=bio, contact_number=contact_number)
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
            subject = data.get('subject')
            status = data.get('status')
            message = data.get('message')
            user = User.objects.get(pk=user_id)
            support_inquiry = SupportInquiry(user=user, subject=subject, message=message, status=status)
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
            user.full_name = data.get('full_name', user.full_name)
            user.role = data.get('role', user.role)
            user.email = data.get('email', user.email)
            user.verified = data.get('verified', user.verified)
            user.password_hash = data.get('password', user.password_hash)
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

            user_id = data.get('user')
            product_id = data.get('product')

            if user_id:
                feedback.user = User.objects.get(pk=user_id)  # Retrieve the User instance

            if product_id:
                feedback.product = Product.objects.get(pk=product_id)  # Retrieve the Product instance

            feedback.comment = data.get('content', feedback.comment)
            feedback.rating = data.get('rating', feedback.rating)

            feedback.save()
            return JsonResponse({'status': 'success', 'message': 'Feedback updated successfully!'})
        except Feedback.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Feedback not found.'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'User not found.'})
        except Product.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Product not found.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'fail', 'message': 'Invalid request method.'})
@csrf_exempt
def update_message(request, message_id):
    if request.method in ['POST', 'PUT']:
        try:
            data = json.loads(request.body)
            message = Message.objects.get(pk=message_id)

            # Update fields as necessary
            message.content = data.get('content', message.content)
            if 'sender_id' in data:
                sender_id = data.get('sender_id')
                sender = User.objects.get(pk=sender_id)
                message.sender = sender
            if 'receiver_id' in data:
                receiver_id = data.get('receiver_id')
                receiver = User.objects.get(pk=receiver_id)
                message.receiver = receiver

            message.save()
            return JsonResponse({'status': 'success', 'message': 'Message updated successfully!'})
        except Message.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Message not found.'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Sender or receiver not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'fail', 'message': 'Invalid request method.'})
    
    
@csrf_exempt
def update_profile(request, profile_id):
    if request.method in ['POST', 'PUT']:
        try:
            data = json.loads(request.body)
            profile = Profile.objects.get(pk=profile_id)
            profile.contact_number = data.get('contact', profile.contact_number)
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

            # Update fields
            if 'subject' in data:
                support_inquiry.subject = data['subject']
            if 'message' in data:
                support_inquiry.message = data['message']
            if 'status' in data:
                support_inquiry.status = data['status']
            if 'user' in data:
                try:
                    new_user = User.objects.get(pk=data['user'])
                    support_inquiry.user = new_user
                except User.DoesNotExist:
                    return JsonResponse({'status': 'fail', 'message': 'User not found.'})

            support_inquiry.save()
            return JsonResponse({'status': 'success', 'message': 'Support Inquiry updated successfully!'})
        except SupportInquiry.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Support Inquiry not found.'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'fail', 'message': 'Invalid JSON.'})
        except Exception as e:
            return JsonResponse({'status': 'fail', 'message': str(e)})
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

@csrf_exempt  # If you're not using the CSRF token, use this decorator
def record_engagement(request):
    if request.method == 'POST':
        try:
            # Parse the request body (assuming JSON format)
            data = json.loads(request.body)
            product_id = data.get('product_id')
            engagement_type = data.get('type')

            # Example logic (you would replace this with your own logic)
            if product_id and engagement_type:
                new_engagement = Engagement.objects.create(
                        product_id=product_id,
                        user_id=1,
                        type=engagement_type
                    )

                    # Save the record (optional since create() automatically saves)
                new_engagement.save()
                return JsonResponse({'status': 'success', 'message': 'Engagement recorded'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Missing parameters'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


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
