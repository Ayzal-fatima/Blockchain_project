from django import forms
from django.contrib.auth.forms import AuthenticationForm





class RegisterFaceForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User ID'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    image = forms.ImageField(help_text="Upload a clear frontal face image.")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("password_confirm")

        if password != confirm_password:
            raise forms.ValidationError("Password and Confirm Password do not match.")


class LoginFaceForm(AuthenticationForm): 
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User ID'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    image = forms.ImageField(help_text="Authenticate using a clear frontal face image.")


