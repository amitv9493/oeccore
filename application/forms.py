from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

class UserForm(UserCreationForm):
    tc = forms.BooleanField(required=True,label='Terms and Conditions')

    email = forms.EmailField(required=True,)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        else:
            return email
            
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=True)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return True