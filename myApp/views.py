from django.shortcuts import render, redirect
from .models import Produce, Farmer, Buyer, CartItem, Profile
from django.contrib.auth.decorators import login_required
from .forms import UserForm, FarmerForm, BuyerForm, ProduceForm
from django.contrib.auth import login, authenticate
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

# Register farmer
def register_farmer(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        farmer_form = FarmerForm(request.POST)
        if user_form.is_valid() and farmer_form.is_valid():
            # Save the user
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            # Check if a Profile already exists for the user
            profile, created = Profile.objects.get_or_create(user=user, defaults={'role': 'farmer'})

            # Automatically make this user a superuser and staff
            #user.is_superuser = True
            #user.is_staff = True

            # Save farmer info
            farmer = farmer_form.save(commit=False)
            farmer.user = user
            farmer.save()

            return redirect('login_farmer')  # Redirect to farmer login page

            # Log in and redirect to farmer dashboard
           # login(request, user)
            #return redirect('farmer_dashboard')
    else:
        user_form = UserForm()
        farmer_form = FarmerForm()
    return render(request, 'myApp/register_farmer.html', {'user_form': user_form, 'farmer_form': farmer_form})


# Register buyer
def register_buyer(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        buyer_form = BuyerForm(request.POST)
        if user_form.is_valid() and buyer_form.is_valid():
            # Save the user
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            # Check if a Profile already exists for the user
            profile, created = Profile.objects.get_or_create(user=user, defaults={'role': 'buyer'})
            
            # Automatically make this user a superuser and staff
            #user.is_superuser = True
            #user.is_staff = True

            # Save buyer info
            buyer = buyer_form.save(commit=False)
            buyer.user = user
            buyer.save()

            return redirect('login_buyer')  # Redirect to buyer login page
    else:
        user_form = UserForm()
        buyer_form = BuyerForm()
    return render(request, 'myApp/register_buyer.html', {'user_form': user_form, 'buyer_form': buyer_form})


# Custom login view for farmers
from .forms import FarmerLoginForm, BuyerLoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

# Custom login view for farmers
def login_farmer(request):
    form = FarmerLoginForm()
    if request.method == 'POST':
        form = FarmerLoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user and user.profile.role == 'farmer':
                login(request, user)
                return redirect('farmer_dashboard')
            else:
                messages.error(request, "Unauthorized access for farmers.")
    return render(request, 'myApp/login_farmer.html', {'form': form})

# Custom login view for buyers
def login_buyer(request):
    form = BuyerLoginForm()
    if request.method == 'POST':
        form = BuyerLoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user and user.profile.role == 'buyer':
                login(request, user)
                return redirect('buyer_dashboard')
            else:
                messages.error(request, "Unauthorized access for buyers.")
    return render(request, 'myApp/login_buyer.html', {'form': form})



# Farmer dashboard view
@login_required
def farmer_dashboard(request):
    
    farmer = Farmer.objects.get(user=request.user)
    produce = Produce.objects.filter(farmer=farmer)
    sales = CartItem.objects.filter(produce__farmer=farmer)  # Tracking sales for the farmer
    return render(request, 'myApp/farmer_dashboard.html', {'produce': produce, 'sales': sales})


# Buyer dashboard view
@login_required
def buyer_dashboard(request):
    produce = Produce.objects.all()  # All available produce for buyers
    return render(request, 'myApp/buyer_dashboard.html', {'produce': produce})


# Register produce by farmer
@login_required
def register_produce(request):
    if request.method == 'POST':
        form = ProduceForm(request.POST, request.FILES)
        if form.is_valid():
            produce = form.save(commit=False)
            produce.farmer = Farmer.objects.get(user=request.user)
            produce.save()
            messages.success(request, 'Produce registered successfully!')
            return redirect('farmer_dashboard')
    else:
        form = ProduceForm()
    return render(request, 'myApp/register_produce.html', {'form': form})


# Add produce to buyer's cart
@login_required
def add_to_cart(request, produce_id):
    buyer = Buyer.objects.get(user=request.user)
    produce = Produce.objects.get(id=produce_id)
    cart_item, created = CartItem.objects.get_or_create(buyer=buyer, produce=produce)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_view')


# View buyer's cart
@login_required
def cart_view(request):
    buyer = Buyer.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(buyer=buyer)
    return render(request, 'myApp/cart_view.html', {'cart_items': cart_items})


# Checkout and clear cart
@login_required
def checkout(request):
    buyer = Buyer.objects.get(user=request.user)
    CartItem.objects.filter(buyer=buyer).delete()
    return render(request, 'myApp/checkout_success.html')

def home(request):
    return render(request, 'myApp/index.html')

def produce_list(request):
    # Display all available produce
    produce = Produce.objects.all()
    return render(request, 'myApp/produce_list.html', {'produce': produce})

from django.shortcuts import render
from .models import Produce

def produce_list(request):
    query = request.GET.get('q')  # Get the search query from the request
    if query:
        all_produce = Produce.objects.filter(name__icontains=query)  # Filter produce by name
    else:
        all_produce = Produce.objects.all()  # Show all produce if no search query

    context = {
        'all_produce': all_produce,
    }
    return render(request, 'myApp/produce_list.html', context)















'''from django.shortcuts import render, redirect
from .models import Produce, Farmer
from django.contrib.auth.decorators import login_required
from .forms import UserForm, FarmerForm, BuyerForm
from django.contrib.auth import login
from .models import Farmer, Buyer
from django.core.exceptions import PermissionDenied
from .models import CartItem
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Produce
from .forms import ProduceForm
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

# Custom login view for farmers
def login_farmer(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.role == 'farmer':
                login(request, user)
                return redirect('farmer_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'myApp/login_farmer.html', {'form': form})

# Custom login view for buyers
def login_buyer(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.role == 'buyer':
                login(request, user)
                return redirect('buyer_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'myApp/login_buyer.html', {'form': form})


# Login view for farmers
class FarmerLoginView(auth_views.LoginView):
    template_name = 'myApp/login_farmer.html'

    def get_success_url(self):
        return reverse_lazy('farmer_dashboard')

# Login view for buyers
class BuyerLoginView(auth_views.LoginView):
    template_name = 'myApp/login_buyer.html'

    def get_success_url(self):
        return reverse_lazy('buyer_dashboard')
    
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import redirect

# Login view for farmers
class FarmerLoginView(LoginView):
    template_name = 'myApp/login_farmer.html'

    def get_success_url(self):
        # Redirect to farmer dashboard after login
        return reverse_lazy('farmer_dashboard')

# Login view for buyers
class BuyerLoginView(LoginView):
    template_name = 'myApp/login_buyer.html'

    def get_success_url(self):
        # Redirect to buyer dashboard after login
        return reverse_lazy('buyer_dashboard')



def register_produce(request):
    if request.method == 'POST':
        form = ProduceForm(request.POST, request.FILES)
        if form.is_valid():
            produce = form.save(commit=False)
            produce.farmer = request.user.farmer  # Assuming farmer is linked to the user
            produce.save()
            messages.success(request, 'Produce registered successfully!')
            return redirect('farmer_dashboard')
    else:
        form = ProduceForm()
    
    return render(request, 'myApp/register_produce.html', {'form': form})

def farmer_dashboard(request):
    print("Farmer dashboard is being called")
    farmer_produce = Produce.objects.filter(farmer=request.user)
    return render(request, 'myApp/farmer_dashboard.html', {'farmer_produce': farmer_produce})

def buyer_dashboard(request):
    all_produce = Produce.objects.all()  # Display all produce for buyers
    return render(request, 'myApp/buyer_dashboard.html', {'all_produce': all_produce})

def home(request):
    return render(request, 'myApp/home.html')

def base(request):
    return render(request, 'myApp/base.html')

@login_required
def farmer_dashboard(request):
    try:
        farmer = Farmer.objects.get(user=request.user)
    except Farmer.DoesNotExist:
        raise PermissionDenied
    produce = Produce.objects.filter(farmer=farmer)
    return render(request, 'myApp/farmer_dashboard.html', {'produce': produce})

@login_required
def add_to_cart(request, produce_id):
    buyer = Buyer.objects.get(user=request.user)
    produce = Produce.objects.get(id=produce_id)
    cart_item, created = CartItem.objects.get_or_create(buyer=buyer, produce=produce)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_view')

@login_required
def cart_view(request):
    buyer = Buyer.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(buyer=buyer)
    return render(request, 'marketplace/cart.html', {'cart_items': cart_items})

@login_required
def checkout(request):
    buyer = Buyer.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(buyer=buyer)
    cart_items.delete()
    return render(request, 'marketplace/checkout_success.html')


@login_required
def buyer_dashboard(request):
    try:
        buyer = Buyer.objects.get(user=request.user)
    except Buyer.DoesNotExist:
        raise PermissionDenied
    produce = Produce.objects.all()
    return render(request, 'myApp/buyer_dashboard.html', {'produce': produce})

def register_farmer(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        farmer_form = FarmerForm(request.POST)
        if user_form.is_valid() and farmer_form.is_valid():
            # Save the user but don't commit to the database yet
            user = user_form.save(commit=False)
            # Set the password for the user
            user.set_password(user_form.cleaned_data['password'])
            # Save the user
            user.save()

            # Check if a Profile already exists for the user
            profile, created = Profile.objects.get_or_create(user=user, defaults={'role': 'farmer'})

            # Save any additional information from farmer_form if needed
            farmer = farmer_form.save(commit=False)
            farmer.user = user
            farmer.save()

            # Automatically log in the user after registration
            login(request, user)

            # Redirect to the farmer's dashboard after registration
            return redirect('farmer_dashboard')
    else:
        user_form = UserForm()
        farmer_form = FarmerForm()

    return render(request, 'myApp/register_farmer.html', {
        'user_form': user_form,
        'farmer_form': farmer_form
    })


def register_buyer(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        buyer_form = BuyerForm(request.POST)
        if user_form.is_valid() and buyer_form.is_valid():
            # Save the user but don't commit to the database yet
            user = user_form.save(commit=False)
            # Set the password for the user
            user.set_password(user_form.cleaned_data['password'])
            # Save the user
            user.save()

            # Check if a Profile already exists for the user
            profile, created = Profile.objects.get_or_create(user=user, defaults={'role': 'buyer'})

            # Save any additional information from buyer_form if needed
            buyer = buyer_form.save(commit=False)
            buyer.user = user
            buyer.save()

            # Automatically log in the user after registration
            login(request, user)

            # Redirect to the buyer's dashboard after registration
            return redirect('buyer_dashboard')
    else:
        user_form = UserForm()
        buyer_form = BuyerForm()

    return render(request, 'myApp/register_buyer.html', {
        'user_form': user_form,
        'buyer_form': buyer_form
    })


def produce_list(request):
    # Display all available produce
    produce = Produce.objects.all()
    return render(request, 'myApp/produce_list.html', {'produce': produce})

@login_required
def farmer_dashboard(request):
    # Only display produce for the logged-in farmer
    farmer = Farmer.objects.get(user=request.user)
    produce = Produce.objects.filter(farmer=farmer)
    return render(request, 'myApp/farmer_dashboard.html', {'produce': produce})

@login_required
def add_produce(request):
    if request.method == "POST":
        farmer = Farmer.objects.get(user=request.user)
        name = request.POST['name']
        price = request.POST['price']
        quantity = request.POST['quantity']
        description = request.POST['description']
        Produce.objects.create(farmer=farmer, name=name, price=price, quantity=quantity, description=description)
        return redirect('farmer_dashboard')
    return render(request, 'myApp/add_produce.html')

@login_required
def buyer_dashboard(request):
    # Display produce to buyers
    produce = Produce.objects.all()
    return render(request, 'myApp/buyer_dashboard.html', {'produce': produce})

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile  # Import Profile model

def login_buyer(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                try:
                    # Check if the authenticated user is a buyer
                    if user.profile.role == 'buyer':
                        login(request, user)
                        return redirect('buyer_dashboard')  # Redirect to buyer dashboard
                    else:
                        messages.error(request, "You are not authorized to access the buyer's login.")
                except Profile.DoesNotExist:
                    messages.error(request, "Profile does not exist for this user.")
            else:
                messages.error(request, "Invalid username or password.")
    return render(request, 'myApp/login_buyer.html', {'form': form})

def login_farmer(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                try:
                    # Check if the authenticated user is a buyer
                    if user.profile.role == 'farmer':
                        login(request, user)
                        return redirect('farmer_dashboard')  # Redirect to buyer dashboard
                    else:
                        messages.error(request, "You are not authorized to access the farmer's login.")
                except Profile.DoesNotExist:
                    messages.error(request, "Profile does not exist for this user.")
            else:
                messages.error(request, "Invalid username or password.")
    return render(request, 'myApp/login_farmer.html', {'form': form})'''
