from django import forms
from django.contrib.auth import get_user_model

class LoginForm(forms.Form):
  username=forms.CharField()
  password=forms.CharField() #もともとあるformsを継承
  
class RegistrationForm(forms.Form):
  username=forms.CharField()
  password=forms.CharField()
  email=forms.EmailField()
  

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'icon', 'introduction')
        widgets = {
            'introduction': forms.Textarea(
                attrs={'rows': 3, 'cols': 50}
            ),
        }