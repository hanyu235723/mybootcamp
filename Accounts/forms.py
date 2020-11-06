from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from django.contrib.auth import get_user_model

User = get_user_model()
class UserEditForm(forms.ModelForm):
    """Form for viewing and editing name fields in a User object.
    A good reference for Django forms is:
    http://pydanny.com/core-concepts-django-modelforms.html
    """

    def __init__(self, *args, **kwargs):
        # TODO: this doesn't seem to work. Need to get to the bottom of it.
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name',  'is_staff', 'is_active', 'date_joined')

    def is_valid(self):
        return super().is_valid()

class SignUpForm(UserCreationForm):
    error_css_class = 'error'
    required_css_class = 'required'

    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.'   )

    class Meta:
        
        model = get_user_model()
        fields = ('first_name', 'last_name', 'date_of_birth' ,'email', 'password1', 'password2')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
                  
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth':forms.SelectDateWidget(),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
             
        }



class myauthenticationForm(AuthenticationForm):
      
    username = UsernameField(widget=forms.EmailInput(attrs={'autofocus': True}))
  
    

    


   
   