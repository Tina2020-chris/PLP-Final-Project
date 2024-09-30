from django import forms
from django.contrib.auth.models import User
from .models import Farmer, Buyer
from django import forms
from .models import Produce
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class FarmerLoginForm(AuthenticationForm):
    """Custom form for farmer login if any customization is needed later."""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your farmer username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
        })
    )


class BuyerLoginForm(AuthenticationForm):
    """Custom form for buyer login if any customization is needed later."""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your buyer username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
        })
    )

class ProduceForm(forms.ModelForm):
    class Meta:
        model = Produce
        fields = ['name', 'price', 'quantity', 'description', 'image']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['farm_name', 'location']

class BuyerForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = ['contact_info']

