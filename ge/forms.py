from django.contrib.auth.forms import AuthenticationForm
from django import forms
from ge.models import Categoria

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario:", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password:", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))

class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria
        fields = ('nom_categoria',)


