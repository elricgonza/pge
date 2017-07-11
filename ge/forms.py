# -*- coding: utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from ge.models import Categoria, Asiento_img
#from versatileimagefield.fields import * #SizedImageCenterpointClickDjangoAdminField, VersatileImageField
from django.forms import ModelForm

'''
class YourModelForm(VersatileImageTestModelForm):
    image = SizedImageCenterpointClickDjangoAdminField(required=False)

    class Meta:
        model = Asiento_img
        fields = ('img',)
'''
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario:", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password:", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ('nom_categoria',)


class SearchForm(forms.Form):
    txt_search = forms.CharField(
        label='Texto para la búsqueda:',
        #widget=forms.TextInput(attrs={'class': 'form-control', 'size': 30, 'autofocus': ''})
        widget=forms.TextInput(attrs={'size': 30, 'autofocus': ''})
    )
