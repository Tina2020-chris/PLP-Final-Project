from django import forms
from django.contrib.auth.models import User
from .models import Farmer, Buyer
from django import forms
from .models import Produce

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

