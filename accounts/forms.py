from django import forms
from.models import AccountsUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User=get_user_model()



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, )
    sap_no =forms.CharField(widget=forms.NumberInput,required=True)
    user_name =forms.CharField(max_length=30, required=True,)
    first_name = forms.CharField(max_length=30, required=False, )
    last_name = forms.CharField(max_length=30, required=False, )
    password1 =forms.PasswordInput()
    password2 =forms.PasswordInput()


    class Meta:
        model = AccountsUser
        fields = ('email','sap_no','user_name', 'first_name', 'last_name',  'password1', 'password2', )