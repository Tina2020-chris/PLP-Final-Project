from django.db import models
from django.contrib.auth.models import User

class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    farm_name = models.CharField(max_length=100,null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.farm_name

class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_info = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.username
    

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('farmer', 'Farmer'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Produce Model: For storing the produce items registered by farmers
class Produce(models.Model):
    FARMER_CATEGORY_CHOICES = [
        ('Vegetable', 'Vegetable'),
        ('Fruit', 'Fruit'),
        ('Grain', 'Grain'),
        ('Dairy', 'Dairy'),
        ('Meat', 'Meat'),
        ('Other', 'Other')
    ]
    
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)  # Farmer who owns this produce
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=FARMER_CATEGORY_CHOICES, default='Other')
    image = models.ImageField(upload_to='produce_images/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)  # Quantity available for sale
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name
    
class Produce(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='produce_images/', blank=True, null=True)

    
    def __str__(self):
        return f"{self.description} by {self.farmer.username}"

    
class CartItem(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    produce = models.ForeignKey(Produce, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.quantity} of {self.produce.name}'


# Order Model: To capture orders made by customers
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('Refunded', 'Refunded'),
        ('On Hold', 'On Hold'),
    ]

    produce = models.ForeignKey(Produce, on_delete=models.CASCADE)  # Link to the produce being ordered
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_orders')  # Customer who made the order
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farmer_orders')  # Farmer selling the produce
    quantity = models.IntegerField()  # Quantity ordered
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Total price of the order
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Pending')  # Order status
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Order #{self.id} by {self.customer.username}"

# SalesData Model: For tracking sales information for dashboard analysis
class SalesData(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)  # Farmer who made the sales
    date = models.DateField()  # Date of sale
    total_items_sold = models.IntegerField()  # Number of items sold on this date
    total_orders = models.IntegerField()  # Number of orders on this date
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)  # Total sales revenue on this date
    
    def __str__(self):
        return f"Sales Data for {self.farmer.username} on {self.date}"

# PageView Model: To capture page views for the dashboard
class PageView(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)
    page_views = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PageViews for {self.farmer.username}: {self.page_views}"

