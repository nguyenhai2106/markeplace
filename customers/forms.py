from django import forms
from accounts.models import User, UserProfile


class UserInforForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']
