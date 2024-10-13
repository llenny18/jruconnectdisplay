from django.db import models

class ProductEngagementSummary(models.Model):
    product_id = models.IntegerField(primary_key=True)
    stock = models.IntegerField()
    user_id = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    image_url = models.URLField(max_length=255, null=True, blank=True)
    date_posted = models.DateTimeField()
    purchase_count = models.IntegerField()
    ad_link = models.URLField(max_length=255, null=True, blank=True)
    fb_link = models.URLField(max_length=255, null=True, blank=True)
    ins_link = models.URLField(max_length=255, null=True, blank=True)
    likes_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'product_engagement_summary'
        
        


class ViewEngagementsByType(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    engagement_count = models.IntegerField()
    type = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'view_engagements_by_type'


class ViewFeedbackByRating(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    rating_count = models.IntegerField()
    rating = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'view_feedback_by_rating'


class ViewProductEngagementOverTime(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    engagement_count = models.IntegerField()
    product_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'view_product_engagement_over_time'


class ViewSupportInquiriesByStatus(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    status_count = models.IntegerField()
    status = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'view_support_inquiries_by_status'


class UserLikes(models.Model):
    like_id = models.AutoField(primary_key=True)  # Use AutoField for auto-incrementing primary key
    user_id = models.IntegerField()
    liker_id = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)  # Automatically set the field to now when the object is created

    class Meta:
        db_table = 'user_likes'
        managed = False  # Set to True if you want Django to manage this table

class User(models.Model):
    USER_ROLES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
    ]

    user_id = models.AutoField(primary_key=True)
    stud_id = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    email = models.EmailField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=USER_ROLES)
    verified = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    profile_url = models.URLField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.full_name} ({self.username})'

    class Meta:
        managed = False
        db_table = 'users'

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    stock = models.IntegerField()
    description = models.TextField()
    category = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    image_url = models.URLField(max_length=255, null=True, blank=True)
    ad_link = models.URLField(max_length=255, null=True, blank=True)
    fb_link = models.URLField(max_length=255, null=True, blank=True)
    ins_link = models.URLField(max_length=255, null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} by {self.user.username}'

    class Meta:
        managed = False
        db_table = 'products'

class Engagement(models.Model):
    ENGAGEMENT_TYPES = [
        ('like', 'Like'),
        ('click', 'Click'),
    ]

    engagement_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=ENGAGEMENT_TYPES)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} {self.get_type_display()} {self.product.title}'

    class Meta:
        managed = False
        db_table = 'engagement'

class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback by {self.user.username} on {self.product.title} - Rating: {self.rating}'

    class Meta:
        managed = False
        db_table = 'feedback'

class UserProductFeedbackView(models.Model):
    user_id = models.IntegerField()
    stud_id = models.IntegerField()
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=7, choices=[('student', 'Student'), ('admin', 'Admin')])
    verified = models.BooleanField(default=False)
    profile_url = models.CharField(max_length=255)
    last_login = models.DateTimeField(null=True, blank=True)
    user_date_created = models.DateTimeField()
    
    product_id = models.IntegerField()
    title = models.CharField(max_length=455)
    description = models.TextField()
    category = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField()
    ad_link = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    image_url = models.CharField(max_length=255, null=True, blank=True)
    date_posted = models.DateTimeField()
    fb_link = models.CharField(max_length=255)
    ins_link = models.CharField(max_length=255)

    feedback_id = models.IntegerField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    feedback_date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_product_feedback_view'

    def __str__(self):
        return f'User {self.username} - Product: {self.title} - Rating: {self.rating}'


class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender.username} to {self.receiver.username}'

    class Meta:
        managed = False
        db_table = 'messages'

class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.URLField(max_length=255, null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

    class Meta:
        managed = False
        db_table = 'profiles'

class SupportInquiry(models.Model):
    INQUIRY_STATUSES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]

    inquiry_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=INQUIRY_STATUSES, default='open')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Inquiry by {self.user.username} on {self.subject} - Status: {self.get_status_display()}'

    class Meta:
        managed = False
        db_table = 'support_inquiries'
