from django import forms
from django.contrib.auth.models import User
from .models import Profile


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control cc-input', 'placeholder': 'First Name'
    }))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control cc-input', 'placeholder': 'Last Name'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control cc-input', 'placeholder': 'Email Address'
    }))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control cc-input', 'placeholder': 'Phone Number'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control cc-input', 'placeholder': 'Password (min 6 chars)'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control cc-input', 'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control cc-input', 'placeholder': 'Username'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control cc-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control cc-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-control cc-input'}),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'city', 'state', 'pincode', 'avatar']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control cc-input'}),
            'address': forms.Textarea(attrs={'class': 'form-control cc-input', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control cc-input'}),
            'state': forms.TextInput(attrs={'class': 'form-control cc-input'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control cc-input'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control cc-input'}),
        }
